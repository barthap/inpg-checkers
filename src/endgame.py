import pygame

from utils.constants import *
import utils.locale as i18n
from scene import BaseScene


# Scene for showing intro
# I created this intro just for demo purposes
class EndGameScene(BaseScene):
	def __init__(self, app, winner_info):
		super().__init__(app)
		self.img = app.resource_manager.get_image('intro.jpg')
		self.img = pygame.transform.scale(self.img, (SCREEN_WIDTH, SCREEN_HEIGHT))
		self.img_rect = self.img.get_rect()
		self.winner = winner_info

	def setup(self):
		self.app.graphics.clear_screen()
		self.app.graphics.draw(self.img, self.img_rect)

		font = pygame.font.SysFont("tahoma", 36)
		font_small = pygame.font.SysFont("tahoma", 24)
		winner_text = font.render(self.winner[1].upper() + " WINS!", True, self.winner[0])
		info_text = font_small.render(i18n.get('any_key'), True, GREEN)

		# Set text coordinates
		text_x = SCREEN_WIDTH / 2 - winner_text.get_width() // 2
		text_y = SCREEN_HEIGHT / 4 - winner_text.get_height() // 2 - 10
		info_x = SCREEN_WIDTH / 2 - info_text.get_width() // 2
		info_y = text_y + 5 + winner_text.get_height()

		self.app.graphics.draw(winner_text, (text_x, text_y))
		self.app.graphics.draw(info_text, (info_x, info_y))

	def update(self, events):
		for event in events:
			if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
				self.app.switch_scene(MENU, True)
