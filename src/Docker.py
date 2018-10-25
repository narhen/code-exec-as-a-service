import docker
from settings import container

class Docker():
    def __init__(self):
        self.docker_client = docker.from_env()

    @property
    def lang_images(self):
        imgs = self.docker_client.images.list()
        return [self.__strip_image_prefix(i.tags[0]) for i in imgs if self.__is_language_image(i.tags)]

    def __is_language_image(self, image_tags):
        return len(image_tags) > 0 and image_tags[0].startswith(container.image.tag_prefix)

    def __strip_image_prefix(self, tag_name):
        return tag_name.replace(container.image.tag_prefix, "")
