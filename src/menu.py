from textmenu_override import supermenu
import os
from datetime import datetime
from typing import List, Tuple


import pygameMenu  # This imports classes and other things
from pygameMenu.locals import *  # Import constants (like actions)

from utils.constants import *
from scene import BaseScene

import utils.locale as i18n
from os import walk
from utils.constants import SAVE_PATH

# Main Menu scene



class MenuScene(BaseScene):
	def __init__(self, app):
		super().__init__(app)

		# Main Menu
		self.menu = pygameMenu.Menu(app.graphics.screen, window_width=SCREEN_WIDTH, window_height=SCREEN_HEIGHT,
									menu_width=SCREEN_WIDTH, menu_height=SCREEN_HEIGHT,
									font=pygameMenu.fonts.FONT_NEVIS,
									title=i18n.get('main_menu'), bgfun=None, dopause=False)

		# Show the rules
		self.help_menu = supermenu(app.graphics.screen, window_width=SCREEN_WIDTH, window_height=SCREEN_HEIGHT,
									menu_width=SCREEN_WIDTH, menu_height=SCREEN_HEIGHT,
									font=pygameMenu.fonts.FONT_FRANCHISE,
									onclose=PYGAME_MENU_DISABLE_CLOSE,
									title=i18n.get('rules_title'), dopause=False,
									menu_color_title=(120, 45, 30),
									menu_color=(30, 50, 107),
									button_region_y=50)

		self.authors_menu = supermenu(app.graphics.screen, window_width=SCREEN_WIDTH, window_height=SCREEN_HEIGHT,
		                           menu_width=SCREEN_WIDTH, menu_height=SCREEN_HEIGHT,
		                           font=pygameMenu.fonts.FONT_FRANCHISE,
		                           onclose=PYGAME_MENU_DISABLE_CLOSE,
                                   text_centered = True,
		                           title=i18n.get('authors'), dopause=False,
		                           menu_color_title=(120, 45, 30),
		                           menu_color=(30, 50, 107),
		                           text_fontsize=40,
		                           button_region_y=50)

		self.load_menu = pygameMenu.Menu(app.graphics.screen, window_width=SCREEN_WIDTH, window_height=SCREEN_HEIGHT,
		                           menu_width=SCREEN_WIDTH, menu_height=SCREEN_HEIGHT,
		                           font=pygameMenu.fonts.FONT_FRANCHISE,
		                           menu_color_title=(120, 45, 30),
		                           menu_color=(30, 50, 107),
		                           title=i18n.get('load_game'), dopause=False)

	@staticmethod
	def list_savegames() -> List[Tuple[str, str, str]]:
		f = []
		for (_, _, filenames) in walk(SAVE_PATH):
			f.extend(filenames)
			break

		saves = []
		for filename in f:
			parts = filename.split('_')
			parts[-1] = parts[-1].split('.')[0]
			parts.append(filename)
			saves.append(tuple(parts[1:]))

		return saves

	def prepare_load_menu(self):
		save_list = self.list_savegames()
		for save in save_list:
			timestamp = float(save[2])
			dt = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
			title = "{} vs {}, {}".format(save[0], save[1], dt)
			self.load_menu.add_option(title, self.__go_play, save[-1])

		self.load_menu.add_option(i18n.get('return_to_menu'), PYGAME_MENU_BACK)

	def setup(self):
		self.app.graphics.clear_screen()

		self.menu.add_option(i18n.get('new_game'), self.__go_play)  # Add timer submenu
		self.menu.add_option(i18n.get('load_game'), self.load_menu)
		self.menu.add_option(i18n.get('rules'), self.help_menu)
		self.menu.add_option(i18n.get('authors'), self.authors_menu)
		self.menu.add_option(i18n.get('exit'), self.app.exit)  # Add exit function


		self.prepare_load_menu()

		rules_path = RESOURCE_PATH + os.sep + i18n.get('rules_filename')
		HELP = open(rules_path, "r")

		for line in HELP:
			self.help_menu.add_line(line)  # Add line
		self.help_menu.add_option(i18n.get('return_to_menu'), PYGAME_MENU_BACK)  # Add option

		HELP.close()


		authors_path = RESOURCE_PATH + os.sep + i18n.get('authors_filename')
		AUTHORS = open(authors_path, "r")

		for line in AUTHORS:
			self.authors_menu.add_line(line)  # Add line
		self.authors_menu.add_option(i18n.get('return_to_menu'), PYGAME_MENU_BACK)  # Add option

		AUTHORS.close()

	def update(self, events):
		self.menu.mainloop(events)
		self.help_menu.main1(events)

	def __go_play(self, load_filename=None):
		self.app.switch_scene(GAME, True, load_filename)
