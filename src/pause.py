import pygame

from utils.constants import *
from scene import BaseScene


class PauseScene(BaseScene):
	def __init__(self, app: 'App'):
		super().__init__(app)
		self.img = app.resource_manager.get_image('pause.jpg')
		self.img = pygame.transform.scale(self.img, (SCREEN_WIDTH, SCREEN_HEIGHT))
		self.img_rect = self.img.get_rect()

	def setup(self):
		self.app.graphics.clear_screen()
		self.app.graphics.draw(self.img, self.img_rect)

		font = pygame.font.SysFont("comicsansms", 24)
		text = font.render("Press space to continue or ESC to return to main menu", True, (0, 255, 0))

		# Set text coordinates
		text_x = SCREEN_WIDTH / 2 - text.get_width() // 2
		text_y = SCREEN_HEIGHT / 4 - text.get_height() // 2

		self.app.graphics.draw(text, (text_x, text_y))

	def update(self, events):
		for event in events:
			if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
				self.app.switch_scene(MENU, reload=True)
			if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
				self.app.switch_scene(GAME, reload=False)
