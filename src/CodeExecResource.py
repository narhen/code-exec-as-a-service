import falcon

class CodeExecResource():
    def __init__(self, docker_client):
        self.docker_client = docker_client

    def on_get(self, req, resp):
        """Get available languages"""
        resp.status = falcon.HTTP_200
        resp.media = self.docker_client.lang_images

