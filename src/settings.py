from os import environ
from addict import Dict

docker_settings = Dict()
docker_settings.image.tag_prefix = "lang:"
# Settings documented here: https://docker-py.readthedocs.io/en/stable/containers.html
docker_settings.container.auto_remove = True
docker_settings.container.cpuset_cpus = "1"
docker_settings.container.init = True
docker_settings.container.network_disabled = True
docker_settings.container.network_mode = "none"
docker_settings.container.privileged = False
docker_settings.container.remove = True
docker_settings.container.restart_policy = {"Name": "no"}
docker_settings.container.read_only = True
docker_settings.container.stdin_open = True
docker_settings.container.tty = False
docker_settings.container.user = 1000
docker_settings.container.working_dir = "/"
docker_settings.container.detach = True
docker_settings.container.command = "sleep 10" # number of seconds the container can live


application = Dict()
application.port = 8080
application.host = "127.0.0.1"
