from os import environ
from addict import Dict

container = Dict()
container.image.tag_prefix = "lang:"

application = Dict()
application.port = 8080
application.host = "127.0.0.1"
