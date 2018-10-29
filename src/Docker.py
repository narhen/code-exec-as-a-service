import docker
from settings import docker_settings as settings

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

    def run_container(self, lang):
        image_name = self.get_image_name(lang)
        return self.docker_client.containers.run(image_name, **settings.container)

