import pygame
import pygame.gfxdraw as _gfxdraw
import pygameMenu.config_textmenu as _cfg
import pygameMenu.config_menu as _cfg_menu
import math
import pygameMenu  # This imports classes and other things
from pygameMenu.locals import *  # Import constants (like actions)
from utils.constants import *  # Import constants (like actions)
import utils.locale as i18n

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
				text_fontsize=20,
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
		self.pages_count = 0
		self.actual_page = 0
		text = self._actual._fonttext.render(LOREM_IPSUM,1, self._actual._font_textcolor)
		text_width_char =math.ceil(text.get_size()[0]/len(LOREM_IPSUM))
		#He is still drunk, but at least he is home
		text_height_char = text.get_size()[1]

		self.char_per_line = (self._width) // (text_width_char)
		self.text_width_char = text_width_char
		self.lines_per_page = (self._height - math.ceil(
			self._actual._title_rect[4][1]) - 2 * text_margin - button_region_y) // (text_height_char)
		self.button_region_y = button_region_y
		self.default_title_str = title
		self.set_title(
			self.default_title_str + " " + i18n.get('page') + ": {actual_page}/{pages_count}".format(actual_page=self.actual_page + 1,
																		pages_count=self.pages_count),
			self._title_offsetx, self._title_offsety)

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
		for linea in self._actual._text[
		             self.actual_page * self.lines_per_page:(self.actual_page + 1) * self.lines_per_page]:
			text = self._actual._fonttext.render(linea, 1,
			                                     self._actual._font_textcolor)

			if self._centered_text:
				text_width = text.get_size()[0]
				text_dx = (self.char_per_line*self.text_width_char/2)-int(text_width / 2.0 + self._actual._pos_text_x)
			else:
				text_dx = 0

			ycoords = self._actual._title_rect[4][1] + self._actual._textdy + dy * (
				self._actual._font_textsize)
			self._surface.blit(text, (self._actual._pos_text_x + text_dx,
			                          ycoords))
			dy += 1

		dysum = 0.5 * self.lines_per_page * (self._actual._font_textsize)

		if(self.actual_page>0):
			instruction1 = "<- " + i18n.get('prev')
			text = self._actual._fonttext.render(instruction1, 1,self._actual._font_textcolor)
			self._surface.blit(text, (self._actual._pos_text_x + 40, ((self._height - (self.lines_per_page
			        * self._actual._font_textsize + self._actual._title_rect[4][1]))/2) - self._actual._font_textsize
			        + (self.lines_per_page * self._actual._font_textsize + self._actual._title_rect[4][1])))

		if(self.actual_page<self.pages_count-1):
			instruction2 = i18n.get('next') + " ->"
			text = self._actual._fonttext.render(instruction2, 1,self._actual._font_textcolor)
			self._surface.blit(text, (self._width-self._actual._pos_text_x - 40 - self.text_width_char
			        * len(instruction2),((self._height- (self.lines_per_page
			        * self._actual._font_textsize + self._actual._title_rect[4][1]))/2) - self._actual._font_textsize
			        + (self.lines_per_page * self._actual._font_textsize + self._actual._title_rect[4][1])))

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

			i=-1
			while(sliced_text_1[i].isalpha()):
				i-=1;
			sliced_text_2=sliced_text_1[self.char_per_line+i:self.char_per_line]+sliced_text_2
			sliced_text_1=sliced_text_1[:self.char_per_line+i]

			self._text.append(sliced_text_1)
			self.add_line(sliced_text_2)
		else:
			self._text.append(text)
		self.pages_count = math.ceil(len(self._text) / self.lines_per_page)
		if self.pages_count < 2:
			self.set_title(self.default_title_str, self._title_offsetx, self._title_offsety)
		else:
			self.set_title(
				self.default_title_str + " " + i18n.get('page') + ": {actual_page}/{pages_count}".format(actual_page=self.actual_page + 1,
																			pages_count=self.pages_count),
				self._title_offsetx, self._title_offsety)

	def main1(self, events=None):
		for event in events:
			if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT and self.actual_page > 0:
				self.actual_page -= 1
				self.set_title(self.default_title_str + " " + i18n.get('page') + ": {actual_page}/{pages_count}".format(
					actual_page=self.actual_page + 1, pages_count=self.pages_count), self._title_offsetx,
									self._title_offsety)

			if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT and self.actual_page < self.pages_count - 1:
				self.actual_page += 1
				self.set_title(self.default_title_str + " " + i18n.get('page') + ": {actual_page}/{pages_count}".format(
					actual_page=self.actual_page + 1, pages_count=self.pages_count), self._title_offsetx,
									self._title_offsety)
