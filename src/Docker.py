import docker
import json
from os import path
from settings import docker_settings as settings, code_exec as exec_settings

class Docker():
    def __init__(self):
        self.docker_client = docker.from_env()

    @property
    def lang_images(self):
        imgs = self.docker_client.images.list()
        return [self.__strip_image_prefix(i.tags[0]) for i in imgs if self.__is_language_image(i.tags)]

    def __is_language_image(self, image_tags):
        return len(image_tags) > 0 and image_tags[0].startswith(settings.image.tag_prefix)

    def __strip_image_prefix(self, tag_name):
        return tag_name.replace(settings.image.tag_prefix, "")

    def get_image_name(self, lang):
        return "{prefix}{lang}".format(prefix=settings.image.tag_prefix, lang=lang)

    def run_container(self, lang, code_dir, mountpoint):
        image_name = self.get_image_name(lang)
        volume = {
                code_dir: {
                    "bind": mountpoint,
                    "mode": "rw"
                }
        }
        return self.docker_client.containers.run(image_name, **settings.container, volumes=volume)

    def build_code(self, container, path):
        return self.__exec(container, "build_program.sh {prog_path}".format(prog_path=path))

    def run_code(self, container, prog_path, prog_input_path=None):
        return self.__exec(container, "run_program.sh {prog_path} {input_path}".format(prog_path=prog_path, input_path=prog_input_path))

    def __read_from_docker_socket(self, sock):
        return b''.join(docker.utils.socket.frames_iter(sock))

    def __exec(self, container, cmd, program_input=None):
        exit_code, output = container.exec_run(cmd, privileged=False, user="user")

        if exit_code is not None and exit_code != 0:
            raise Exception("Something went wrong when executing. Exit code = {}, output = '{}'".format(exit_code, output))
        try:
            return json.loads(output.decode("utf-8"))
        except Exception as e:
            return {
                    "status": "error",
                    "message": "Failed to decode json in response from container: '{}'. Response was '{}'".format(e, output),
            }

