import pygame

from textmenu_override import supermenu
import os
from datetime import datetime
from typing import List, Tuple


import pygameMenu  # This imports classes and other things
from pygameMenu.locals import *  # Import constants (like actions)

from utils.constants import *
from scene import BaseScene

import utils.locale as i18n
import utils.config as config
from os import walk
from utils.constants import SAVE_PATH


# Main Menu scene
from utils.text import TextInput

__actualpath = str(os.path.abspath(
    os.path.dirname(__file__))).replace('\\', '/')
__fontdir = '{0}/fonts/{1}.ttf'
class MenuScene(BaseScene):
	def __init__(self, app):
		super().__init__(app)

		# Main Menu
		self.menu = pygameMenu.Menu(app.graphics.screen, window_width=SCREEN_WIDTH, window_height=SCREEN_HEIGHT,
									menu_width=SCREEN_WIDTH, menu_height=SCREEN_HEIGHT,
									font=FONT_MENU,
									title=i18n.get('main_menu'), bgfun=None, dopause=False)

		self.settings_menu= pygameMenu.Menu(app.graphics.screen, window_width=SCREEN_WIDTH, window_height=SCREEN_HEIGHT,
		                            menu_width=SCREEN_WIDTH, menu_height=SCREEN_HEIGHT,
		                            font=FONT_MENU,
		                            title=i18n.get('settings'), bgfun=None, dopause=False)

		self.settings_checkers_count_menu = pygameMenu.Menu(app.graphics.screen, window_width=SCREEN_WIDTH,
		                                     window_height=SCREEN_HEIGHT,
		                                     menu_width=SCREEN_WIDTH, menu_height=SCREEN_HEIGHT,
		                                     font=FONT_MENU,
		                                     title=i18n.get('checkers_count'), bgfun=None, dopause=False)

		self.settings_sound_menu = pygameMenu.Menu(app.graphics.screen, window_width=SCREEN_WIDTH,
		                                                    window_height=SCREEN_HEIGHT,
		                                                    menu_width=SCREEN_WIDTH, menu_height=SCREEN_HEIGHT,
		                                                    font=FONT_MENU,
		                                                    title=i18n.get('sound'), bgfun=None, dopause=False)

		self.settings_language_menu = pygameMenu.Menu(app.graphics.screen, window_width=SCREEN_WIDTH,
		                                           window_height=SCREEN_HEIGHT,
		                                           menu_width=SCREEN_WIDTH, menu_height=SCREEN_HEIGHT,
		                                           font=FONT_MENU,
		                                           title=i18n.get('language'), bgfun=None, dopause=False)

		self.settings_players_names_menu = pygameMenu.Menu(app.graphics.screen, window_width=SCREEN_WIDTH,
		                                              window_height=SCREEN_HEIGHT,
		                                              menu_width=SCREEN_WIDTH, menu_height=SCREEN_HEIGHT,
		                                              font=FONT_MENU,
		                                              title=i18n.get('Players_Names'), bgfun=None, dopause=False)
		self.settings_game_time_menu = pygameMenu.Menu(app.graphics.screen, window_width=SCREEN_WIDTH,
		                                                   window_height=SCREEN_HEIGHT,
		                                                   menu_width=SCREEN_WIDTH, menu_height=SCREEN_HEIGHT,
		                                                   font=FONT_MENU,
		                                                   title=i18n.get('game_time'), bgfun=None, dopause=False)

		# Show the rules
		self.help_menu = supermenu(app.graphics.screen, window_width=SCREEN_WIDTH, window_height=SCREEN_HEIGHT,
									menu_width=SCREEN_WIDTH, menu_height=SCREEN_HEIGHT,
									font=FONT_TEXT,
                                    font_title=FONT_MENU,
									onclose=PYGAME_MENU_DISABLE_CLOSE,
									title=i18n.get('rules_title'), dopause=False,
									menu_color_title=(120, 45, 30),
									menu_color=(30, 50, 107),
									button_region_y=50)

		self.authors_menu = supermenu(app.graphics.screen, window_width=SCREEN_WIDTH, window_height=SCREEN_HEIGHT,
		                           menu_width=SCREEN_WIDTH, menu_height=SCREEN_HEIGHT,
		                           font=FONT_TEXT,
		                           font_title=FONT_MENU,
		                           onclose=PYGAME_MENU_DISABLE_CLOSE,
                                   text_centered = True,
		                           title=i18n.get('authors'), dopause=False,
		                           menu_color_title=(120, 45, 30),
		                           menu_color=(30, 50, 107),
		                           text_fontsize=40,
		                           button_region_y=50)

		self.load_menu = pygameMenu.Menu(app.graphics.screen, window_width=SCREEN_WIDTH, window_height=SCREEN_HEIGHT,
		                           menu_width=SCREEN_WIDTH, menu_height=SCREEN_HEIGHT,
		                           font=FONT_TEXT,
		                           menu_color_title=(120, 45, 30),
		                           menu_color=(30, 50, 107),
		                           title=i18n.get('load_game'), dopause=False)

		self.init()

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
		for save in save_list[-7:]:
			timestamp = float(save[2])
			dt = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
			title = "{} vs {}, {}".format(save[0], save[1], dt)
			self.load_menu.add_option(title, self.__go_play, save[-1])

		self.load_menu.add_option(i18n.get('return_to_menu'), PYGAME_MENU_BACK)

	def init(self):
		self.app.graphics.clear_screen()

		sound_opts = [(i18n.get('on'), 'yes'),  # 0th option
		              (i18n.get('off'), 'no')]  # 1st option
		# if sounds is yes, default option is 0th, else 1st
		default_sound = 0 if config.get('general', 'sounds').lower() == 'yes' else 1

		checkers_count_opts = [(i18n.get('2_rows'), '2'),
		                       (i18n.get('3_rows'), '3')]
		default_rows = 0 if config.get('general', 'startpiecerows') == '2' else 1

		lang_opts = [('English', 'english'),
		              ('Polski', 'polish')]

		default_lang = 0 if config.get('general', 'locale').lower() == 'english' else 1


		self.menu.add_option(i18n.get('new_game'), self.__go_play)  # Add timer submenu
		self.menu.add_option(i18n.get('load_game'), self.load_menu)
		self.menu.add_option(i18n.get('rules'), self.help_menu)
		self.menu.add_option(i18n.get('settings'), self.settings_menu_in)
		self.menu.add_option(i18n.get('authors'), self.authors_menu)
		self.menu.add_option(i18n.get('exit'), self.app.exit)  # Add exit function

		self.settings_menu.add_selector(i18n.get('checkers_count'), checkers_count_opts,
		                                onreturn=None, onchange=self.__change_checkers_rows, default=default_rows)
		self.settings_menu.add_selector(i18n.get('sound'), sound_opts,
		                                onreturn=None, onchange=self.__change_sound, default=default_sound)
		self.settings_menu.add_selector(i18n.get('language'), lang_opts,
		                                onreturn=self.__change_lang, onchange=None, default=default_lang)


		self.settings_menu.add_option(i18n.get('Players_Names'), self.settings_players_names_menu)
		self.settings_menu.add_option(i18n.get('return_to_menu'), self.settings_menu_out)
		self.settings_menu.disable()

		self.settings_players_names_menu.add_option('BLUE', self.__change_player, BLUE)
		self.settings_players_names_menu.add_option('RED', self.__change_player, RED)
		self.settings_players_names_menu.add_option(i18n.get('return_to_menu'), PYGAME_MENU_BACK)


		self.prepare_load_menu()

		rules_path = RESOURCE_PATH + os.sep + i18n.get('rules_filename')
		HELP = open(rules_path, "r",encoding='utf-8')

		for line in HELP:
			self.help_menu.add_line(line)  # Add line
		self.help_menu.add_option(i18n.get('return_to_menu'), PYGAME_MENU_BACK)  # Add option

		HELP.close()

		authors_path = RESOURCE_PATH + os.sep + i18n.get('authors_filename')
		AUTHORS = open(authors_path, "r",encoding='utf-8')

		for line in AUTHORS:
			self.authors_menu.add_line(line)  # Add line
		self.authors_menu.add_option(i18n.get('return_to_menu'), PYGAME_MENU_BACK)  # Add option

		AUTHORS.close()

	def update(self, events):
		self.app.graphics.clear_screen()
		if self.menu.is_enabled():
			self.menu.mainloop(events)
			self.help_menu.main1(events)
		elif self.settings_menu.is_enabled():
			self.settings_menu.mainloop(events)

	def settings_menu_in(self):
		self.menu.disable()
		self.settings_menu.enable()

	def settings_menu_out(self):
		self.menu.enable()
		self.settings_menu.disable()

	def __go_play(self, load_filename=None):
		self.app.switch_scene(GAME, True, load_filename)

	def __change_player(self, color):
		name_opt = 'blue_name' if color == BLUE else 'red_name'
		player_name = config.get('general', name_opt)
		scene = PlayerNamesScene(self.app, player_name, color)
		self.app.scene_manager.go_once(scene)

	@staticmethod
	def __change_sound(opt):
		cfg = config.get('general')
		cfg['sounds'] = opt
		config.save()

	def __change_lang(self, opt):
		i18n.switch_language(opt)
		config.save()
		self.app.switch_scene(MENU, True)


	@staticmethod
	def __change_checkers_rows(opt):
		cfg = config.get('general')
		cfg['startpiecerows'] = opt
		config.save()


class PlayerNamesScene(BaseScene):
	def __init__(self, app, name, color):
		super().__init__(app)
		self.nameString = name
		self.color = color
		self.textInput = TextInput(default_text=name, text_color=color, font_family="comicsansms", cursor_color=color)

	def update(self, events):
		font = pygame.font.SysFont("tahoma", 32)
		text = font.render('Enter player name', True, WHITE)    # TODO: ADD TRANSLATION HERE!
		text_x = SCREEN_WIDTH/2 - text.get_width() //2

		self.app.graphics.clear_screen()
		self.app.graphics.draw(text, (text_x, 10))

		for event in events:
			if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
				self.save()
				return
			if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
				self.back()
				return

		self.textInput.update(events)
		text_surf: pygame.Surface = self.textInput.get_surface()
		text_x = SCREEN_WIDTH / 2 - text_surf.get_width() // 2
		self.app.graphics.draw(text_surf, (text_x, 50))

	def save(self):
		name_opt = 'blue_name' if self.color == BLUE else 'red_name'
		cfg = config.get('general')
		cfg[name_opt] = self.textInput.get_text()
		config.save()
		self.app.switch_scene(MENU, False)

	def back(self):
		self.app.switch_scene(MENU, False)
