import falcon
import tempfile
from json import loads
from os import path
from shutil import rmtree
import base64

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
            code = loads(req.bounded_stream.read())

            source_code = base64.b64decode(bytearray(code["source"], "utf-8"))
            inputs = code.get("inputs", [])

            resp.media = self._build_and_run_code(source_code, lang, inputs)
            resp.status = falcon.HTTP_200
        except Exception as e:
            print(str(e))
            resp.media = self._create_error("Internal server error", str(e))
            resp.status = falcon.HTTP_500

    def _build_and_run_code(self, code, lang, inputs):
        code_path, code_filename = self._create_tmp_dir(code)
        mountpoint = "/mnt"
        container = self.docker_client.run_container(lang, code_path, mountpoint)
        build_status = self._build_code(container, code_path, code_filename, mountpoint)
        if build_status["status"] != "ok":
            return build_status

        outputs = []
        for program_input in inputs:
            output = self._exec_code(container, code_path, build_status["outfile"], mountpoint, program_input)
            outputs.append({"input": program_input, "output": output})

        ret = rmtree(code_path)
        container.kill()

        return outputs

    def _exec_code(self, container, code_path, executable, mountpoint, program_input):
        program_output = self.docker_client.run_code(container, path.join(mountpoint, executable), program_input)
        output = self._read_file(code_path, program_output["outfile"])
        return self._create_error("OK", "Successfully executed code", output)

    def _build_code(self, container, code_path, code_filename, mountpoint):
        build_status = self.docker_client.build_code(container, path.join(mountpoint, code_filename))
        if build_status["status"].lower() != "ok":
            message = build_status.get("message") or "There was a build error"
            output = self._read_file(code_path, build_status.get("outfile"))
            return self._create_error("BUILD_ERROR", message, output)
        return build_status

    def _create_tmp_dir(self, code):
        tmp_path = tempfile.mkdtemp()
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
