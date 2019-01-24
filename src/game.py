import errno
import math
import os
import random
from collections import namedtuple
import pickle
from copy import copy, deepcopy
from time import time

import pygame

from utils.resources import ResourceManager
from scene import BaseScene
from utils.constants import *
from graphics import Graphics
from typing import Tuple, List, Set
import utils.config as cfg
import utils.locale as i18n
from utils.time import GameTimer

# Type definitions
Coords = Tuple[int, int]
Color = Tuple[int, int, int]
SquareMatrix = List[List['Square']]
GameInfo = namedtuple('GameInfo', ['turn', 'time', 'start_msg'])

TEXT_X = BOARD_SIZE + 20
x_center = lambda t: BOARD_SIZE + 200 / 2 - t.get_width() // 2

BEGIN_MESSAGE_DURATION = 3  # in seconds

# it is later read from config / loaded savegame
blue_name = 'BLUE'
red_name = 'RED'
num_piece_rows = 3
sounds = False


# Main Game code
class GameScene(BaseScene):
	def __init__(self, app: 'App', load_name=None):
		super().__init__(app)
		self.renderer = GameRenderer(app.graphics)
		self.resource_manager = ResourceManager()
		self.selected_square: Square = None  # Board square
		self.timer = GameTimer()
		self.begin_msg = True
		self.game_ended = False

		global blue_name, red_name, num_piece_rows, sounds
		blue_name = cfg.get('general', 'blue_name')
		red_name = cfg.get('general', 'red_name')
		num_piece_rows = int(cfg.get('GENERAL', 'StartPieceRows'))
		sounds = cfg.get('general').getboolean('sounds')

		self.board: Board = Board()

		# Randomly select first turn
		self.turn: Color = BLUE if bool(random.getrandbits(1)) else RED

		if load_name is not None:
			self.load_game(load_name)

	def save_game(self) -> None:
		print("Saving game...")
		game_state = {
			"board": self.board,
			"turn": self.turn,
			"blue_name": blue_name,
			"red_name": red_name,
			"time": self.timer.get()
		}

		if not os.path.exists(SAVE_PATH):
			try:
				os.makedirs(SAVE_PATH)
			except OSError as e:
				if e.errno != errno.EEXIST:
					raise

		filename = SAVE_PATH + os.sep + "save_{}_{}_{}.dat".format(blue_name, red_name, int(time()))

		with open(filename, 'wb') as file:
			pickle.dump(game_state, file, protocol=pickle.HIGHEST_PROTOCOL)
			print("Saved!")

	def load_game(self, filename: str) -> None:
		global blue_name, red_name
		print("Loading game...")
		self.deselect_piece()
		self.begin_msg = False
		with open(SAVE_PATH + os.sep + filename, 'rb') as file:
			loaded_state = pickle.load(file)
			board = loaded_state['board']
			turn = loaded_state['turn']
			blue_name = loaded_state['blue_name']
			red_name = loaded_state['red_name']
			self.timer.restart(int(loaded_state['time']))
			self.turn = copy(turn)
			self.board = deepcopy(board)
			print("Game loaded successfully")

	def select_piece(self) -> None:
		mouse_square: Square = self.mouse_in_what_square()  # just make a variable once
		if mouse_square is not None and mouse_square.piece is not None and mouse_square.piece.color == self.turn:
			# Somebody else can hop but not me:
			if self.can_anyone_hop() and not self.can_hop(mouse_square.location):
				print("Other piece can HOP!")
				if sounds:
					self.resource_manager.get_sound('err.wav').play()
			else:
				self.update_selected(mouse_square)

	def update_selected(self, new_square: 'Square') -> None:
		self.selected_square = new_square
		self.selected_square.highlighted = True
		print("selected", self.selected_square.location)

		legal_moves = self.board.legal_moves(self.selected_square.location)
		if len(legal_moves) > 0:
			print('legal:')
			for location in legal_moves:
				print(location)
				self.board[location].highlighted = True
		else:
			print('no legal moves')
			if sounds:
				self.resource_manager.get_sound('err2.wav').play()
			self.deselect_piece()

	def deselect_piece(self) -> None:
		self.board.remove_all_highlights()
		self.selected_square = None
		print("unselected")

	def move_piece(self) -> None:
		mouse_square = self.mouse_in_what_square()
		if self.selected_square is not None:
			if mouse_square == self.selected_square:
				print('same, deselecting')
				self.deselect_piece()

			if mouse_square is not None and mouse_square.color == BLACK and mouse_square.piece is None:
				if mouse_square.location in self.board.legal_moves(self.selected_square.location):
					if self.can_hop():  # Hop an enemy
						enemy_pos = self.board.enemy_between(self.selected_square.location, mouse_square.location)
						enemy_piece = self.board.get_square(enemy_pos)
						print("HOPPED AN ENEMY!")
						self.play_piece_sound(True)
						self.board.remove_piece(enemy_piece)  # Remove an enemy
						self.board.remove_all_highlights()  # Remove old highlights
						mouse_square.piece = self.selected_square.piece
						self.board.remove_piece(self.selected_square)
						self.update_selected(mouse_square)
						if not self.can_hop():
							self.deselect_piece()
							self.switch_turn()
					else:
						self.play_piece_sound(False)
						mouse_square.piece = self.selected_square.piece
						self.board.remove_piece(self.selected_square)
						self.deselect_piece()
						self.switch_turn()

	# If location argument is empty, it checks currently selected_square
	def can_hop(self, location: Coords = None) -> bool:
		if location is None:
			if self.selected_square is None:
				return False
			location = self.selected_square.location

		if not self.board[location].piece.king:
			adj = self.board.adjacent_tiles(location)
			for move in self.board.legal_moves(location):
				if move not in adj:
					return True
			return False
		else:  # king = True
			return len(self.board.hop_possible_squares(location)) > 0

	# Can anyone hop in this turn
	def can_anyone_hop(self) -> bool:
		for (x, y) in Board.all_board_coords():
			sq = self.board[(x, y)]
			if sq.piece is not None and sq.piece.color == self.turn:
				if self.can_hop((x, y)):
					return True
		return False

	# Returns True if any piece with specified color can do a legal move
	def can_anyone_move(self, turn: Color) -> bool:
		if self.board.knight_possible():
			return True

		squares = list()

		# Firstly get all squares with pieces matching turn color
		for pos in Board.all_board_coords():
			sq = self.board.get_square(pos)
			if sq.piece is not None and sq.piece.color == turn:
				squares.append(sq)

		for sq in squares:
			# Somebody has more than 0 legal moves - so he can move
			if len(self.board.legal_moves(sq.location)) > 0:
				return True

		return False

	# Returns True if there are any pieces with specified color left
	def has_any_pieces(self, turn: Color) -> bool:
		for pos in Board.all_board_coords():
			sq = self.board.get_square(pos)
			if sq.piece is not None and sq.piece.color == turn:
				return True
		return False

	# Returns True if end game and Winner color, otherwise False and None
	def is_end_game(self) -> (bool, Color):
		# If blue hasn't got pieces or cannot move - Red wins
		if not (self.can_anyone_move(BLUE) and self.has_any_pieces(BLUE)):
			return True, RED

		# If red hasn't got pieces or cannot move - Blue wins
		if not (self.can_anyone_move(RED) and self.has_any_pieces(RED)):
			return True, BLUE

		# Not yet end game
		return False, None

	def switch_turn(self) -> None:
		end_game, winner = self.is_end_game()
		if end_game is True:
			self.game_ended = True
			print("END GAME,", ("RED" if winner == RED else "BLUE"), "Wins!")
			if sounds is True:
				self.resource_manager.get_sound('end_game.wav').play()

			winner_name = blue_name if winner == BLUE else red_name
			self.app.switch_scene(END_GAME, True, (winner, winner_name))
		else:
			self.turn = BLUE if self.turn == RED else RED  # if red then blue, else RED xD
			print("Current turn: " + ("RED" if self.turn == RED else "BLUE"))

	def play_piece_sound(self, hop=False) -> None:
		if not sounds:
			return

		if self.selected_square.piece.king is True:
			if hop:
				self.resource_manager.get_sound('king_hop.wav').play()
			else:
				self.resource_manager.get_sound('king.wav').play()
		else:
			if hop:
				self.resource_manager.get_sound('hop.wav').play()
			else:
				self.resource_manager.get_sound('move.wav').play()

	def setup(self):
		pass

	def update(self, events) -> None:
		pressed = pygame.key.get_pressed()

		alt_held = pressed[pygame.K_LALT] or pressed[pygame.K_RALT]
		ctrl_held = pressed[pygame.K_LCTRL] or pressed[pygame.K_RCTRL]
		for event in events:
			if event.type == pygame.KEYDOWN and (event.key == pygame.K_SPACE or event.key == pygame.K_ESCAPE) \
					and not self.begin_msg:
				self.timer.pause()
				self.app.switch_scene(PAUSE)
				return
			if event.type == pygame.KEYDOWN and (event.key == pygame.K_s) and ctrl_held:
				self.save_game()
			elif event.type == pygame.KEYDOWN and (event.key == pygame.K_l) and ctrl_held:
				pass
			if event.type == pygame.MOUSEBUTTONDOWN:
				if self.begin_msg is True:
					self.begin_msg = False
					self.timer.restart()
				if self.selected_square is None:
					self.select_piece()
				else:
					self.move_piece()
		if self.board.knight_possible() and sounds is True:
			self.resource_manager.get_sound('promote.wav').play()

		if self.game_ended is True:
			self.timer.pause()
			return

		if self.timer.is_paused is True and not self.begin_msg:
			self.timer.resume()

		if self.begin_msg is True and self.timer.current_time >= BEGIN_MESSAGE_DURATION:
			self.begin_msg = False
			self.timer.restart(0)

		game_info = GameInfo(turn=self.turn, time=self.timer.get(), start_msg=self.begin_msg)
		self.renderer.render_screen(self.board, game_info)

	def mouse_in_what_square(self) -> 'Square':
		sq_pos = what_square(pygame.mouse.get_pos())
		return self.board[sq_pos] if self.board.is_on_board(sq_pos) else None


class GameRenderer:
	def __init__(self, graphics: Graphics):
		resource_manager = ResourceManager()
		self.graphics = graphics

		# background
		self.bg = resource_manager.get_image('board.png')
		self.bg_rect = self.bg.get_rect()

		# pieces
		self.red_piece = resource_manager.get_image('redpiece.png')
		self.blue_piece = resource_manager.get_image('bluepiece.png')
		self.blue_king = resource_manager.get_image('blueking.png')
		self.red_king = resource_manager.get_image('redking.png')

		# Sidebar
		self.side_img = resource_manager.get_image('sidebar_bg.jpg')
		self.side_font = pygame.font.SysFont("tahoma", 16, True)
		self.side_bg = self.prepare_side_bg()
		self.small_blue = pygame.transform.scale(self.blue_piece, (30, 30))
		self.small_red = pygame.transform.scale(self.red_piece, (30, 30))
		self.turn_text = self.side_font.render(i18n.get('turn'), True, BROWN)

		# start game message
		self.message_font = pygame.font.SysFont("tahoma", 48, True)

	def generate_bg(self) -> None:
		self.graphics.clear_screen()
		self.graphics.draw(self.bg, self.bg_rect)
		self.graphics.draw(self.side_bg, (BOARD_SIZE, 0))

	def prepare_side_bg(self) -> pygame.Surface:
		side_bg = pygame.Surface((SCREEN_WIDTH - BOARD_SIZE, SCREEN_HEIGHT))
		side_bg.fill(GREEN)

		side_rect = side_bg.get_rect()
		img_rect = self.side_img.get_rect()
		sw = side_rect.w
		sh = side_rect.h
		iw = img_rect.w
		ih = img_rect.h

		num_horizontal = int(math.ceil(sw / iw))
		num_vertical = int(math.ceil(sh / ih))
		for x in range(num_horizontal):
			for y in range(num_vertical):
				side_bg.blit(self.side_img, pygame.Rect(x * iw, y * ih, iw, ih))

		info_text = self.side_font.render(i18n.get('pause_info'), True, BROWN)
		# load_text = self.side_font.render(i18n.get('load_info'), True, BROWN)
		save_text = self.side_font.render(i18n.get('save_info'), True, BROWN)
		side_bg.blit(info_text, (20, SCREEN_HEIGHT - 30))
		side_bg.blit(save_text, (20, SCREEN_HEIGHT - 35 - info_text.get_height()))
		# side_bg.blit(save_text, (20, SCREEN_HEIGHT - 40 - 2*load_text.get_height()))

		return side_bg

	def render_screen(self, board: 'Board', info: GameInfo) -> None:
		self.generate_bg()
		self.draw_highlighted_squares(board)
		self.draw_board_pieces(board)
		self.draw_sidebar_info(info)

		if info.start_msg is True:
			player_name = blue_name if info.turn == BLUE else red_name
			msg_text = self.message_font.render(i18n.get('start_msg').format(player_name), True, info.turn)
			pos_x = BOARD_SIZE / 2 - msg_text.get_width() // 2
			pos_y = BOARD_SIZE / 2 - msg_text.get_height() // 2
			self.graphics.draw(msg_text, (pos_x, pos_y))

	def draw_sidebar_info(self, info: GameInfo):
		turn_name = i18n.get('BLUE') if info.turn == BLUE else i18n.get('RED')
		current_turn_text = self.side_font.render(turn_name, True, info.turn)

		secs = info.time % 60
		mins = (info.time - secs) // 60
		if info.start_msg is True:
			time_text = self.side_font.render("00:00", True, BROWN)
		else:
			time_text = self.side_font.render("{:02d}:{:02d}".format(mins, secs), True, BROWN)
		self.graphics.draw(time_text, (x_center(time_text), 20))

		player_color = lambda t: t if info.turn == t else BROWN
		blue_player = self.side_font.render(blue_name, True, player_color(BLUE))
		red_player = self.side_font.render(red_name, True, player_color(RED))

		self.graphics.draw(self.turn_text, (TEXT_X, 60))
		self.graphics.draw(current_turn_text, (TEXT_X + self.turn_text.get_width() + 5, 60))

		blue_y = 145
		red_y = 100

		if info.turn == BLUE:
			pass
			cy = blue_y + self.small_blue.get_height() // 2
		else:
			cy = red_y + self.small_red.get_height() // 2

		pygame.draw.circle(self.graphics.screen, YELLOW, (TEXT_X + self.small_red.get_width() // 2, cy),
		                   self.small_red.get_width() // 2 + 5, 5)

		self.graphics.draw(self.small_blue, (TEXT_X, blue_y))
		self.graphics.draw(self.small_red, (TEXT_X, red_y))

		name_x = TEXT_X + self.small_blue.get_width() + 10
		height_center = self.small_blue.get_height() // 2 - blue_player.get_height() // 2
		self.graphics.draw(blue_player, (name_x, blue_y + height_center))
		self.graphics.draw(red_player, (name_x, red_y + height_center))

	def draw_board_pieces(self, board: 'Board') -> None:
		for (x, y) in Board.all_board_coords():
			if board[(x, y)].piece is not None:
				if board[(x, y)].piece.color == RED and not board[(x, y)].piece.king:
					self.graphics.draw(self.red_piece, what_pixel((x, y)))
				elif board[(x, y)].piece.color == RED and board[(x, y)].piece.king:
					self.graphics.draw(self.red_king, what_pixel((x, y)))
				elif board[(x, y)].piece.color == BLUE and board[(x, y)].piece.king:
					self.graphics.draw(self.blue_king, what_pixel((x, y)))
				elif board[(x, y)].piece.color == BLUE and not board[(x, y)].piece.king:
					self.graphics.draw(self.blue_piece, what_pixel((x, y)))

	def draw_highlighted_squares(self, board: 'Board', color=GREEN) -> None:
		rect_surface = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE))
		rect_surface.set_alpha(128)  # 0 = przezeroczysty, 255 = pelny
		rect_surface.fill(color)
		for x in range(8):
			for y in range(8):
				pos = (x, y)
				if board.get_square(pos).highlighted:
					self.graphics.draw(rect_surface, what_pixel(pos))


# Returns top left pixel of specified board tile
def what_pixel(board_coords: Coords) -> Tuple[int, int]:
	return board_coords[0] * SQUARE_SIZE, board_coords[1] * SQUARE_SIZE


def what_square(pixel_coord: Tuple[int, int]) -> Coords:
	return int(pixel_coord[0] / SQUARE_SIZE), int(pixel_coord[1] / SQUARE_SIZE)


# Used only to generate Board.all_board_coords()
def board_black_tile_coords() -> Set[Coords]:
	black_coords = set()
	for x in range(8):
		for y in range(8):
			pos = (x, y)
			if ((x % 2 != 0) and (y % 2 != 0)) or ((x % 2 == 0) and (y % 2 == 0)):
				black_coords.add(pos)
	return black_coords


class Board:
	def __init__(self):
		self.matrix: SquareMatrix = self.generate_board_matrix()

	def get_square(self, coords: Coords) -> 'Square':
		(x, y) = coords
		if not self.is_on_board(coords):
			raise IndexError("Coords " + str(coords) + " are outside of board")

		return self.matrix[x][y]

	# Allows using board[coords] or board[(x, y)] instead of board.get_square(...), earlier matrix_coords()
	def __getitem__(self, item: Coords) -> 'Square':
		return self.get_square(item)

	@staticmethod
	def remove_piece(square: 'Square') -> None:
		square.piece = None

	@staticmethod
	def generate_board_matrix() -> SquareMatrix:
		board_matrix: SquareMatrix = [[None] * 8 for _ in range(8)]

		for x in range(8):
			for y in range(8):
				pos = (x, y)
				if (x % 2 != 0) and (y % 2 == 0):
					board_matrix[x][y] = Square(WHITE, pos)
				elif (x % 2 != 0) and (y % 2 != 0):
					board_matrix[x][y] = Square(BLACK, pos)
				elif (x % 2 == 0) and (y % 2 != 0):
					board_matrix[x][y] = Square(WHITE, pos)
				elif (x % 2 == 0) and (y % 2 == 0):
					board_matrix[x][y] = Square(BLACK, pos)

		for x in range(8):
			for y in range(num_piece_rows):
				if board_matrix[x][y].color == BLACK:
					board_matrix[x][y].piece = Piece(RED)
			for y in range(8 - num_piece_rows, 8):
				if board_matrix[x][y].color == BLACK:
					board_matrix[x][y].piece = Piece(BLUE)

		return board_matrix

	# Returns collection of all valid (black tile) coords
	# Made this method to avoid using two range 8 for loops:
	# for x in range(8):
	#    for y in range(8):
	#       ...
	# It is hardcoded and was generated using board_black_tile_coords()
	# usage:
	# for coords in Board.all_board_coords():
	#     ...
	# or
	# for (x, y) in Board.all_board_coords():
	#     ...
	@staticmethod
	def all_board_coords() -> Set[Coords]:
		return {(7, 3), (1, 3), (6, 6), (7, 7), (6, 2), (5, 1), (3, 7), (2, 4), (4, 0), (3, 3), (5, 5), (4, 4), (1, 5),
		        (2, 2), (0, 4), (1, 1), (6, 4), (0, 0), (2, 6), (7, 1), (6, 0), (7, 5), (4, 2), (3, 5), (5, 3), (4, 6),
		        (3, 1), (5, 7), (0, 6), (2, 0), (1, 7), (0, 2)}

	def remove_all_highlights(self) -> None:
		for x in range(8):
			for y in range(8):
				self.matrix[x][y].highlighted = False

	# Used for finding enemy position when hopping
	def enemy_between(self, piece_pos: Coords, mouse_pos: Coords) -> Coords:
		(px, py) = piece_pos
		(mx, my) = mouse_pos
		if px > mx and py > my:
			direction = NW
		elif px > mx and py < my:
			direction = SW
		elif px < mx and py < my:
			direction = SE
		else:
			direction = NE

		enemy_pos = piece_pos
		# iterates fields in direction: Piece pos ---> Mouse pos
		for i in range(1, 8):
			enemy_pos = self.squares_in_dir(piece_pos, direction, i)
			if self.is_on_board(enemy_pos) and self.get_square(enemy_pos).piece is not None:
				break

		# if its still the same, an enemy wasn't found
		assert enemy_pos != piece_pos
		return enemy_pos

	# Returns coordinates of tile relative ('number' fields away) to a position in specified direction
	# DOES NOT CHECK IF ON BOARD!
	@staticmethod
	def squares_in_dir(position: Coords, direction, number: int = 1) -> Coords:
		(x, y) = position
		if direction == NW:
			return x - number, y - number
		if direction == NE:
			return x + number, y - number
		if direction == SE:
			return x + number, y + number
		if direction == SW:
			return x - number, y + number

	# Returns coordinates of all tiles adjacent to specified position
	# DOES NOT CHECK IF ON BOARD!
	@staticmethod
	def adjacent_tiles(pos: Coords) -> List[Coords]:
		return [Board.squares_in_dir(pos, NE),
		        Board.squares_in_dir(pos, NW),
		        Board.squares_in_dir(pos, SE),
		        Board.squares_in_dir(pos, SW)]

	@staticmethod
	def is_on_board(coords: Coords) -> bool:
		(x, y) = coords
		return not (x < 0 or y < 0 or x > 7 or y > 7)

	# TODO: move possible squares for king
	def move_possible_squares(self, coords: Coords) -> List[Coords]:
		(x, y) = coords
		piece: Piece = self.matrix[x][y].piece
		normal_legal_moves = list()

		if piece is not None:
			if piece.king is False:
				if piece.color == BLUE:
					nw_dir = self.squares_in_dir(coords, NW, 1)
					if self.is_on_board(nw_dir) and self.get_square(nw_dir).piece is None:
						normal_legal_moves.append(nw_dir)

					ne_dir = self.squares_in_dir(coords, NE, 1)
					if self.is_on_board(ne_dir) and self.get_square(ne_dir).piece is None:
						normal_legal_moves.append(ne_dir)
				elif piece.color == RED:
					sw_dir = self.squares_in_dir(coords, SW, 1)
					if self.is_on_board(sw_dir) and self.get_square(sw_dir).piece is None:
						normal_legal_moves.append(sw_dir)

					se_dir = self.squares_in_dir(coords, SE, 1)
					if self.is_on_board(se_dir) and self.get_square(se_dir).piece is None:
						normal_legal_moves.append(se_dir)
			# If king is True
			if piece.king:
				normal_legal_moves.extend(self.king_move_tiles(coords))

		return normal_legal_moves

	def legal_moves(self, coords: Coords) -> List[Coords]:
		legal_moves = list()
		legal_moves.extend(self.move_possible_squares(coords))
		hop_moves = self.hop_possible_squares(coords)
		if len(hop_moves) > 0:
			legal_moves = hop_moves

		return legal_moves

	def king_move_tiles(self, coords: Coords) -> List[Coords]:
		possible_squares = list()
		for direction in [NW, SW, NE, SE]:
			for number in range(8):  # 0-7 tiles away
				tile_pos: Coords = self.squares_in_dir(coords, direction, number)
				if self.is_on_board(tile_pos):
					next_tile_pos = self.squares_in_dir(tile_pos, direction, 1)
					next_tile_on_board = self.is_on_board(next_tile_pos)
					next_tile_has_piece = (next_tile_on_board and self.get_square(next_tile_pos).piece is not None)
					if tile_pos != coords:  # moving nowhere is illegal
						possible_squares.append(tile_pos)
					if (next_tile_on_board and next_tile_has_piece) or \
							(next_tile_on_board is False):
						break
		return possible_squares

	def hop_possible_squares(self, coords: Coords) -> List[Coords]:
		hop_moves = []
		(x, y) = coords
		piece: Piece = self.matrix[x][y].piece

		if piece is not None:
			if not piece.king:
				for move in self.adjacent_tiles(coords):
					if move is not None and self.is_on_board(move):
						# If on adjacent tile there is an enemy
						if self.get_square(move).piece is not None and self.get_square(
								move).piece.color != self.get_square(coords).piece.color:
							# Position one behind enemy
							pos_behind = (move[0] + (move[0] - coords[0]), move[1] + (move[1] - coords[1]))
							if self.is_on_board(pos_behind) and self.get_square(pos_behind).piece is None:
								hop_moves.append(pos_behind)

			else:  # elif piece.king is True:
				(x, y) = coords
				for direction in [NW, SW, NE, SE]:
					for number in range(8):
						tile: (x, y) = self.squares_in_dir(coords, direction, number)
						if self.is_on_board(tile):
							next_tile_pos = self.squares_in_dir(tile, direction, 1)
							if self.is_on_board(next_tile_pos):
								next_tile: Square = self.get_square(next_tile_pos)
								if next_tile.piece is not None and next_tile.piece.color != piece.color:
									do_break = False
									for arg in range(8):  # iterating tiles behind enemy
										tile_after_pos = self.squares_in_dir(next_tile.location, direction, arg)
										if self.is_on_board(tile_after_pos):
											tile_after: Square = self.get_square(tile_after_pos)
											if tile_after.piece is None:
												hop_moves.append(tile_after_pos)
											else:
												if arg > 0:  # arg = 0 is hopped enemy
													do_break = True
													break
									if do_break:
										break
								elif next_tile.piece is not None and next_tile.piece.color == piece.color:
									break

		return hop_moves

	def knight_possible(self) -> bool:
		somebody_promoted = False
		for x in range(8):
			for y in range(7, 8):
				piece: Piece = self.matrix[x][y].piece
				if piece is not None and piece.color == RED and not piece.king:
					piece.king = True
					somebody_promoted = True
			for y in range(1):
				piece: Piece = self.matrix[x][y].piece
				if piece is not None and piece.color == BLUE and not piece.king:
					piece.king = True
					somebody_promoted = True
		return somebody_promoted


class Square:
	def __init__(self, color: Color, location: Coords, piece=None):
		self.color: Color = color
		self.piece: 'Piece' = piece
		self.location: Coords = location
		self.highlighted: bool = False

	def __str__(self):
		return ("BLACK " if self.color == BLACK else "WHITE ") + " Square at " + str(self.location) + ", " + \
		       ("not " if not self.highlighted else "") + "highlighted"


class Piece:
	def __init__(self, color: Color, king=False):
		self.color: Color = color
		self.king: bool = king

	def __str__(self):
		return ("RED " if self.color == BLACK else "BLUE ") + ("King" if self.king else "Piece")
