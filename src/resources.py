import pygame
import os

from constants import *


# This class is used to load images (and in future other resources) only once and keep their reference in memory
# Also, it simplifies loading resource methods
class ResourceManager:
    def __init__(self):
        self.__image_library = {}

    # Use this to load image
    def get_image(self, path):
        image = self.__image_library.get(path)      # Try to get image from library (maybe its already loaded)

        # If not, then load it
        if image is None:
            img_path = RESOURCE_PATH + os.sep + IMAGE_PATH + os.sep + path
            canonical_path = img_path.replace('/', os.sep).replace('\\', os.sep)
            image = pygame.image.load(canonical_path)
            self.__image_library[path] = image

        return image
