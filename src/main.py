#!/usr/bin/env python

from gevent.pywsgi import WSGIServer
from falcon import API

from Docker import Docker
from CodeExecResource import CodeExecResource
from settings import application

def main():
    docker_client = Docker()
    code_exec_handler = CodeExecResource(docker_client)

    app = API()
    app.add_route("/exec", code_exec_handler)
    WSGIServer((application.host, application.port), app).serve_forever()

if __name__ == "__main__":
    main()
