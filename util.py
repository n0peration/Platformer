import pyglet
import config

def load_image(path):
    return pyglet.resource.image(config.IMG_DIR + path)
