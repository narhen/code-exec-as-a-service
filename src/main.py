#!/usr/bin/env python

from gevent.pywsgi import WSGIServer
from falcon import API

from Docker import Docker
from CodeExecResource import CodeExec, Languages
from settings import application

def main():
    docker_client = Docker()
    languages_handler = Languages(docker_client)
    code_exec_handler = CodeExec(docker_client)

    app = API()
    app.add_route("/exec/{lang}", code_exec_handler)
    app.add_route("/", languages_handler)
    WSGIServer((application.host, application.port), app).serve_forever()

if __name__ == "__main__":
    main()
