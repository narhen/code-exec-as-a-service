import falcon
import tempfile
import base64
import traceback
from json import loads
from os import path, unlink
from shutil import rmtree
from settings import application as app_settings


class Languages:
    def __init__(self, docker_client):
        self.docker_client = docker_client

    def on_get(self, req, resp):
        """Get available languages"""
        resp.status = falcon.HTTP_200
        resp.media = self.docker_client.lang_images

class CodeExec:
    def __init__(self, docker_client):
        self.docker_client = docker_client

    def on_post(self, req, resp, lang):
        if lang not in self.docker_client.lang_images:
            message = "language '{}' is not supported".format(lang)
            resp.media = self._create_error("UNSUPPORTED LANGUAGE", message)
            resp.status = falcon.HTTP_400
            return

        try:
            code = loads(req.bounded_stream.read().decode("utf-8"))

            source_code = base64.b64decode(bytearray(code["source"], "utf-8"))
            inputs = code.get("inputs", [])

            status_code, output = self._build_and_run_code(source_code, lang, inputs)
            resp.media = output
            resp.status = status_code
        except Exception as e:
            traceback.print_exc()
            print(str(e))
            resp.media = self._create_error("Internal server error", str(e))
            resp.status = falcon.HTTP_500

    def _build_and_run_code(self, code, lang, inputs):
        code_path, code_filename = self._create_tmp_dir(code)
        mountpoint = app_settings.code_base_mount_dir
        container = self.docker_client.run_container(lang, code_path, mountpoint)
        build_status = self._build_code(container, code_path, code_filename, mountpoint)
        if build_status["status"] != "ok":
            rmtree(code_path)
            container.kill()
            return falcon.HTTP_400, build_status

        outputs = []
        for program_input in inputs:
            output = self._exec_code(container, code_path, build_status["outfile"], mountpoint, program_input)
            outputs.append({"input": program_input, "output": output})

        rmtree(code_path)
        container.kill()

        return falcon.HTTP_200, outputs

    def _exec_code(self, container, code_path, executable, mountpoint, program_input):
        host_input_path = path.join(code_path, app_settings.input_filename)
        with open(host_input_path, "wb") as f:
            f.write(bytes(program_input, "utf-8"))

        prog_path = path.join(mountpoint, executable)
        input_path = path.join(mountpoint, app_settings.input_filename)
        program_output = self.docker_client.run_code(container, prog_path, input_path)
        unlink(host_input_path)

        if program_output.get("status", "ok").lower() == "error":
            message = program_output.get("message", "Internal server error")
            return self._create_error("ERROR", "Failed to run code", message)

        output = self._read_file(code_path, program_output["outfile"])
        return self._create_error("OK", "Successfully executed code", output)

    def _build_code(self, container, code_path, code_filename, mountpoint):
        build_status = self.docker_client.build_code(container, path.join(mountpoint, code_filename))
        if build_status["status"].lower() != "ok":
            message = build_status.get("message") or "There was a build error"

            outfile = build_status.get("outfile")
            if outfile:
                output = self._read_file(code_path, outfile)
            else:
                output = None
            return self._create_error("BUILD_ERROR", message, output)
        return build_status

    def _create_tmp_dir(self, code):
        tmp_path = tempfile.mkdtemp(dir=app_settings.tmp_dir)
        code_filename = "code"

        with open(path.join(tmp_path, code_filename), "w") as fh:
            fh.write(code.decode("utf-8"))

        return tmp_path, code_filename

    def _read_file(self, dirname, filename):
        with open(path.join(dirname, filename), "r") as fh:
            return fh.read()

    def _create_error(self, status, message, output=None):
        return {
            "status": status,
            "message": message,
            "output": output,
        }
