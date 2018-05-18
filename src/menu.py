import pygame
import pygameMenu                # This imports classes and other things
from pygameMenu.locals import *  # Import constants (like actions)

from constants import *
from scene import BaseScene
from game import GameScene
import pygame.gfxdraw as _gfxdraw
import pygameMenu.config_textmenu as _cfg
import pygameMenu.config_menu as _cfg_menu
import math


# Main Menu scene
class supermenu(pygameMenu.TextMenu):
	def __init__(self,
                 surface,
                 window_width,
                 window_height,
                 font,
                 title,
	             button_region_y=0,
                 draw_text_region_x=_cfg.TEXT_DRAW_X,
                 text_centered=_cfg.TEXT_CENTERED,
                 text_color=_cfg.TEXT_FONT_COLOR,
                 text_fontsize= 20,
                 text_margin=_cfg.TEXT_MARGIN,
                 **kwargs):
		super(supermenu,self).__init__(
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
				** kwargs)
		self.pages_count = 0
		self.actual_page = 0
		text = self._actual._fonttext.render("A", 1,self._actual._font_textcolor)
		text_width_char = text.get_size()[0];
		text_height_char = self._actual._font_textsize
		self.char_per_line = (self._width) // (text_width_char)
		self.lines_per_page = (self._height- math.ceil(self._actual._title_rect[4][1])-2*text_margin-button_region_y) // (text_height_char)
		self.button_region_y=button_region_y
	def draw(self):
		assert isinstance(self._actual, supermenu)

		# Draw background rectangle
		_gfxdraw.filled_polygon(self._surface, self._actual._bgrect,
		                        self._actual._bgcolor)
		# Draw title
		_gfxdraw.filled_polygon(self._surface, self._actual._title_rect,
		                        self._bg_color_title)
		self._surface.blit(self._actual._title, self._title_pos)

		# Draw text
		dy = 0
		for linea in self._actual._text[0:self.lines_per_page]:
			text = self._actual._fonttext.render(str(dy)+" "+linea, 1,
			                                     self._actual._font_textcolor)
			text_width = text.get_size()[0]

			ycoords =  self._actual._title_rect[4][1]+ self._actual._textdy+ dy * (
					self._actual._font_textsize)
			#ycoords -= self._actual._font_textsize / 2
			self._surface.blit(text, (self._actual._pos_text_x,
			                          ycoords))
			dy += 1

		dysum =   0.5*dy * (self._actual._font_textsize)

		dy = 0
		dy_index = 0
		for option in self._actual._option:
			# If option is selector
			if option[0] == PYGAMEMENU_TYPE_SELECTOR:
				# If selected index then change color
				if dy == self._actual._index:
					text = self._actual._font.render(option[1].get(), 1,
					                                 self._actual._sel_color)
					text_bg = self._actual._font.render(option[1].get(), 1,
					                                    _cfg_menu.SHADOW_COLOR)
				else:
					text = self._actual._font.render(option[1].get(), 1,
					                                 self._actual._font_color)
					text_bg = self._actual._font.render(option[1].get(), 1,
					                                    _cfg_menu.SHADOW_COLOR)
			else:
				# If selected index then change color
				if dy == self._actual._index:
					text = self._actual._font.render(option[0], 1,
					                                 self._actual._sel_color)
					text_bg = self._actual._font.render(option[0], 1,
					                                    _cfg_menu.SHADOW_COLOR)
				else:
					text = self._actual._font.render(option[0], 1,
					                                 self._actual._font_color)
					text_bg = self._actual._font.render(option[0], 1,
					                                    _cfg_menu.SHADOW_COLOR)
			# Text font and size
			text_width, text_height = text.get_size()
			if self._actual._centered_option:
				text_dx = -int(text_width / 2.0)
				t_dy = -int(text_height / 2.0)
			else:
				text_dx = 0
				t_dy = 0
			# Draw fonts
			if self._actual._option_shadow:
				ycoords = self._actual._opt_posy + dy * (
						self._actual._fsize + self._actual._opt_dy) + t_dy - 3
				self._surface.blit(text_bg,
				                   (self._actual._opt_posx + text_dx - 3,
				                    ycoords + dysum))
			ycoords = self._actual._opt_posy + dy * (
					self._actual._fsize + self._actual._opt_dy) + t_dy
			self._surface.blit(text, (self._actual._opt_posx + text_dx,
			                          ycoords + dysum))
			# If selected option draw a rectangle
			if self._actual._drawselrect and (dy_index == self._actual._index):
				if not self._actual._centered_option:
					text_dx_tl = -text_width
				else:
					text_dx_tl = text_dx
				ycoords = self._actual._opt_posy + dy * (
						self._actual._fsize + self._actual._opt_dy) + t_dy - 2
				pygame.draw.line(self._surface, self._actual._sel_color, (
					self._actual._opt_posx + text_dx - 10,
					self._actual._opt_posy + dysum + dy * (
							self._actual._fsize + self._actual._opt_dy) + t_dy - 2),
				                  ((self._actual._opt_posx - text_dx_tl + 10,
				                    ycoords + dysum)), self._actual._rect_width)
				ycoords = self._actual._opt_posy + dy * (
						self._actual._fsize + self._actual._opt_dy) - t_dy + 2
				pygame.draw.line(self._surface, self._actual._sel_color, (
					self._actual._opt_posx + text_dx - 10,
					self._actual._opt_posy + dysum + dy * (
							self._actual._fsize + self._actual._opt_dy) - t_dy + 2),
				                  ((self._actual._opt_posx - text_dx_tl + 10,
				                    ycoords + dysum)), self._actual._rect_width)
				ycoords = self._actual._opt_posy + dy * (
						self._actual._fsize + self._opt_dy) - t_dy + 2
				pygame.draw.line(self._surface, self._actual._sel_color, (
					self._actual._opt_posx + text_dx - 10,
					self._actual._opt_posy + dysum + dy * (
							self._actual._fsize + self._actual._opt_dy) + t_dy - 2),
				                  ((self._actual._opt_posx + text_dx - 10,
				                    ycoords + dysum)), self._actual._rect_width)
				ycoords = self._actual._opt_posy + dy * (
						self._actual._fsize + self._actual._opt_dy) - t_dy + 2
				pygame.draw.line(self._surface, self._actual._sel_color, (
					self._actual._opt_posx - text_dx_tl + 10,
					self._actual._opt_posy + dysum + dy * (
							self._actual._fsize + self._actual._opt_dy) + t_dy - 2),
				                  ((self._actual._opt_posx - text_dx_tl + 10,
				                    ycoords + dysum)), self._actual._rect_width)
			dy += 1
			dy_index += 1

	def add_line(self, text):
		text = text.strip()
		if len(text) > self.char_per_line:
			sliced_text_1 = text[:self.char_per_line]
			sliced_text_2 = text[self.char_per_line:]

			if(sliced_text_1[-1].isalpha()):
				sliced_text_2=sliced_text_1[-1]+sliced_text_2
				sliced_text_1=sliced_text_1[:-1]+'-'
			self._text.append(sliced_text_1)
			self.add_line(sliced_text_2)
		else:
			self._text.append(text)
		self.pages_count = len(self._text) // self.lines_per_page

class MenuScene(BaseScene):
    def __init__(self, app):
        super().__init__(app)

        # Main Menu
        self.menu = pygameMenu.Menu(app.graphics.screen, window_width=SCREEN_WIDTH, window_height=SCREEN_HEIGHT,
                                menu_width=SCREEN_WIDTH, menu_height=SCREEN_HEIGHT,
                                font=pygameMenu.fonts.FONT_NEVIS,
                                title='Menu Gry', bgfun=None, dopause=False)

        # Show the rules
        self.help_menu = supermenu(app.graphics.screen, window_width=SCREEN_WIDTH, window_height=SCREEN_HEIGHT,
                                        menu_width=SCREEN_WIDTH, menu_height=SCREEN_HEIGHT,
                                        font=pygameMenu.fonts.FONT_FRANCHISE,
                                        onclose=PYGAME_MENU_DISABLE_CLOSE,
                                        title='Help', dopause=False,
                                        menu_color_title=(120, 45, 30),
                                        menu_color=(30, 50, 107),
                                   button_region_y=50)

    def setup(self):
        self.app.graphics.clear_screen()

        self.menu.add_option('Play', self.__go_play)  # Add timer submenu
        self.menu.add_option('Rules', self.help_menu)
        self.menu.add_option('Exit', self.app.exit)  # Add exit function

        HELP = open("resources/rules.txt","r")

        for line in HELP:
            self.help_menu.add_line(line)  # Add line
        self.help_menu.add_option('Return to Menu',  PYGAME_MENU_BACK)  # Add option

    def update(self, events):
        self.menu.mainloop(events)

    def __go_play(self):
        self.app.switch_state(GameScene(self.app))
