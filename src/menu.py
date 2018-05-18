import pygame
import pygameMenu  # This imports classes and other things
from pygameMenu.locals import *  # Import constants (like actions)

from constants import *
from scene import BaseScene
from game import GameScene
import pygameMenu.config_textmenu as _cfg


# Main Menu scene
class supermenu(pygameMenu.TextMenu):
	def __init__(self,
	             surface,
	             window_width,
	             window_height,
	             font,
	             title,
	             draw_text_region_x=_cfg.TEXT_DRAW_X,
	             text_centered=_cfg.TEXT_CENTERED,
	             text_color=_cfg.TEXT_FONT_COLOR,
	             text_fontsize=_cfg.MENU_FONT_TEXT_SIZE,
	             text_margin=_cfg.TEXT_MARGIN,
	             **kwargs):
		super(supermenu, self).__init__(
			surface,
			window_width,
			window_height,
			font,
			title,
			draw_text_region_x,
			text_centered,
			text_color,
			text_fontsize,
			text_margin,
			**kwargs)


class MenuScene(BaseScene):
	def __init__(self, app):
		super().__init__(app)

		# Main Menu
		self.menu = pygameMenu.Menu(app.graphics.screen, window_width=SCREEN_WIDTH, window_height=SCREEN_HEIGHT,
		                            font=pygameMenu.fonts.FONT_NEVIS,
		                            title='Menu Gry', bgfun=None, dopause=False)

		# Show the rules
		self.help_menu = supermenu(app.graphics.screen, window_width=SCREEN_WIDTH, window_height=SCREEN_HEIGHT,
		                           font=pygameMenu.fonts.FONT_FRANCHISE,
		                           onclose=PYGAME_MENU_DISABLE_CLOSE,
		                           title='Help', dopause=False,
		                           menu_color_title=(120, 45, 30),
		                           menu_color=(30, 50, 107))

	def setup(self):
		self.app.graphics.clear_screen()

		self.menu.add_option('Play', self.__go_play)  # TODO: Add timer submenu
		self.menu.add_option('Rules', self.help_menu)
		self.menu.add_option('Exit', self.app.exit)

		HELP = open("resources/rules.txt", "r")

		for line in HELP:
			self.help_menu.add_line(line)  # Add line
		self.help_menu.add_option('Return to Menu', PYGAME_MENU_BACK)  # Add option

	def update(self, events):
		self.menu.mainloop(events)

	def __go_play(self):
		self.app.switch_scene(GAME)
