#!/usr/bin/env python
import docker
from sys import exit
from gevent.pywsgi import WSGIServer
from falcon import API

from Docker import Docker
from CodeExecResource import CodeExec, Languages
from settings import application

def docker_is_available():
    try:
        docker.from_env().info()
        return True
    except Exception as e:
        print(str(e))
        return False

def main():
    if not docker_is_available():
        print("Docker does not seem to be available..")
        return 1
    docker_client = Docker()
    languages_handler = Languages(docker_client)
    code_exec_handler = CodeExec(docker_client)

    app = API()
    app.add_route("/exec/{lang}", code_exec_handler)
    app.add_route("/", languages_handler)

    print("Starting on {host}:{port}".format(host=application.host, port=application.port))
    WSGIServer((application.host, application.port), app).serve_forever()

    return 0

if __name__ == "__main__":
    exit(main())
