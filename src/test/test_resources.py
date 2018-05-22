import unittest
from os import listdir
from os.path import isfile, join
import os
import pathlib

import pygame

from utils.constants import *
from utils.resources import ResourceManager

images_path = RESOURCE_PATH + os.sep + IMAGE_PATH


class ResourceTests(unittest.TestCase):
	def setUp(self):
		self.manager = ResourceManager()

	def test_loadExisting(self):
		imgs = [f for f in listdir(images_path) if isfile(join(images_path, f))]
		if len(imgs) == 0:
			raise Exception("Couldn't test, there are no images in " + images_path)

		# Take first existing image and try to load it
		img_path = pathlib.Path(imgs[0])
		image = self.manager.get_image(img_path.name)

		self.assertIsInstance(image, pygame.Surface)

	def test_doesNotExist(self):
		with self.assertRaises(FileNotFoundError):
			self.manager.get_image("file_that_doesnt_exist.for_sure")


if __name__ == "__main__":
	unittest.main()
