import falcon
import tempfile
from os import path
from shutil import rmtree

class CodeExecResource():
    def __init__(self, docker_client):
        self.docker_client = docker_client

    def on_get(self, req, resp):
        """Get available languages"""
        resp.status = falcon.HTTP_200
        resp.media = self.docker_client.lang_images

    def on_post(self, req, resp):
        try:
            code = req.bounded_stream.read()
            resp.media = self._build_and_run_code(code)

            resp.status = falcon.HTTP_200
        except Exception as e:
            resp.media = {
                    "status": "Internal server error",
                    "output": str(e)
            }
            resp.status = falcon.HTTP_500

    def _build_and_run_code(self, code):
        code_path, code_filename = self._create_tmp_dir(code)
        mountpoint = "/mnt"
        container = self.docker_client.run_container("C", code_path, mountpoint)

        output = self._exec_code(container, code_path, code_filename, mountpoint)

        ret = rmtree(code_path)
        container.kill()

        return output

    def _exec_code(self, container, code_path, code_filename, mountpoint):
        build_status = self.docker_client.build_code(container, path.join(mountpoint, code_filename))
        if build_status["status"].lower() != "ok":
            return {
                    "status": "BUILD_ERROR",
                    "message": build_status.get("message") or "There was a build error",
                    "output": self._read_file(code_path, build_status.get("outfile")),
            }

        program_output = self.docker_client.run_code(container, path.join(mountpoint, build_status["outfile"]))
        return {
                "status": "OK",
                "output": self._read_file(code_path, program_output["outfile"]),
        }

    def _create_tmp_dir(self, code):
        tmp_path = tempfile.mkdtemp()
        code_filename = "code"

        with open(path.join(tmp_path, code_filename), "w") as fh:
            fh.write(code.decode("utf-8"))

        return tmp_path, code_filename

    def _read_file(self, dirname, filename):
        with open(path.join(dirname, filename), "r") as fh:
            return fh.read()
