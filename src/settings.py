from os import environ
from addict import Dict

docker_settings = Dict()
docker_settings.image.tag_prefix = "lang:" # The prefix to look for in docker image tags
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
docker_settings.container.command = "sleep {seconds}".format(seconds=60*1) # number of seconds the container can live


application = Dict()
application.port = int(environ.get("PORT", "8080"))
application.host = environ.get("HOST", "0.0.0.0")
application.tmp_dir = environ.get("TMP_DIRECTORY", "/tmp") # must be a one-to-one mapping from the host filesystem
application.code_base_mount_dir = "/mnt" # base directory in which client code will be mounted (inside language docker containers)

code_exec = Dict() # settings for executing user code
code_exec.read_timeout = 1.0 # max time (seconds) to wait for program output
code_exec.max_output_length = 8192 # maximum ouput length (bytes). Set to None for infinite length
