import pygame

from resources import ResourceManager
from scene import BaseScene
from constants import *
from graphics import Graphics
from typing import Tuple, List

# Type definitions
Coords = Tuple[int, int]
Color = Tuple[int, int, int]
SquareMatrix = List[List['Square']]

# Try with 2 ;)
# tutaj zmieniać, jeżeli w opcjach zostanie zmieniony wariant gry pomięddzy 2-3 rzędy
num_piece_rows = 3


# Main Game code
class GameScene(BaseScene):
	def __init__(self, app: 'App'):
		super().__init__(app)
		self.renderer = GameRenderer(app.graphics, app.resource_manager)
		self.board: Board = Board()
		self.turn: Color = BLUE
		self.selected_square: Square = None  # Board square

	def select_piece(self):
		mouse_square: Square = self.mouse_in_what_square()  # just make a variable once
		if mouse_square.piece is not None and mouse_square.piece.color == self.turn:
			self.selected_square = mouse_square
			self.selected_square.highlighted = True
			print("selected", self.selected_square.location)
			print('legal:')
			for items in self.board.legal_moves(self.selected_square.location):
				print(items)

	def deselect_piece(self):
		self.selected_square.highlighted = False
		self.selected_square = None
		print("unselected")

	def move_piece(self):
		mouse_square = self.mouse_in_what_square()
		if self.selected_square is not None:
			if mouse_square == self.selected_square:
				self.deselect_piece()

			# TODO: force hop if any piece can do it

			if mouse_square.color is BLACK and mouse_square.piece is None:
				if mouse_square.location in self.board.legal_moves(self.selected_square.location):
					mouse_square.piece = self.selected_square.piece
					self.board.remove_piece(self.selected_square)
					self.deselect_piece()
					self.switch_turn()

	def switch_turn(self):
		self.turn = BLUE if self.turn is RED else RED  # if red then blue, else RED xD
		print("Current turn: " + ("RED" if self.turn is RED else "BLUE"))

	def setup(self):
		pass

	def update(self, events):
		for event in events:
			if event.type == pygame.MOUSEBUTTONDOWN:
				if self.selected_square is None:
					self.select_piece()
				else:
					self.move_piece()
		self.renderer.render_screen(self.board)

	def mouse_in_what_square(self) -> 'Square':
		return self.board.matrix_coords(what_square(pygame.mouse.get_pos()))


class GameRenderer:
	def __init__(self, graphics: Graphics, resource_manager: ResourceManager):
		self.graphics = graphics
		self.bg = resource_manager.get_image('board.png')
		self.bg_rect = self.bg.get_rect()
		self.redpiece = resource_manager.get_image('redpiece.png')
		self.bluepiece = resource_manager.get_image('bluepiece.png')
		self.blueking = resource_manager.get_image('blueking.png')
		self.redking = resource_manager.get_image('redking.png')

	def generate_bg(self) -> None:
		self.graphics.clear_screen()
		self.graphics.draw(self.bg, self.bg_rect)

	def render_screen(self, board: 'Board') -> None:
		self.generate_bg()
		self.draw_highlighted_squares(board)
		self.draw_board_pieces(board)

	# tutaj dodawać funkcje rysujące na ekran

	def draw_board_pieces(self, board: 'Board') -> None:
		for x in range(8):
			for y in range(8):
				if board.matrix_coords((x, y)).piece is not None:
					if board.matrix_coords((x, y)).piece.color == RED and board.matrix_coords(
							(x, y)).piece.king == False:
						self.graphics.draw(self.redpiece, what_pixel((x, y)))
					elif board.matrix_coords((x, y)).piece.color == RED and board.matrix_coords(
							(x, y)).piece.king == True:
						self.graphics.draw(self.redking, what_pixel((x, y)))
					elif board.matrix_coords((x, y)).piece.color == BLUE and board.matrix_coords(
							(x, y)).piece.king == True:
						self.graphics.draw(self.blueking, what_pixel((x, y)))
					elif board.matrix_coords((x, y)).piece.color == BLUE and board.matrix_coords(
							(x, y)).piece.king == False:
						self.graphics.draw(self.bluepiece, what_pixel((x, y)))

	def draw_highlighted_squares(self, board: 'Board', color=GREEN) -> None:
		rect_surface = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE))
		rect_surface.set_alpha(128)  # 0 = przezeroczysty, 255 = pelny
		rect_surface.fill(color)
		for x in range(8):
			for y in range(8):
				pos = (x, y)
				if board.matrix_coords(pos).highlighted is True:
					self.graphics.draw(rect_surface, what_pixel(pos))


def what_pixel(board_coords: Coords) -> Tuple[int, int]:
	# zwraca górny lewy pixel danego pola planszy
	return board_coords[0] * SQUARE_SIZE, board_coords[1] * SQUARE_SIZE


def what_square(pixel_coord: Tuple[int, int]) -> Coords:
	return int(pixel_coord[0] / SQUARE_SIZE), int(pixel_coord[1] / SQUARE_SIZE)


class Board:
	def __init__(self):
		self.matrix: SquareMatrix = self.generate_board_matrix()

	def matrix_coords(self, coords: Coords) -> 'Square':
		return self.matrix[coords[0]][coords[1]]

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

	def squares_in_dir(self, position: Coords, direction, number: int) -> Coords:
		(x, y) = position
		if direction == NW and self.is_on_board((x - number, y - number)):
			return x - number, y - number
		if direction == NE and self.is_on_board((x + number, y - number)):
			return x + number, y - number
		if direction == SE and self.is_on_board((x + number, y + number)):
			return x + number, y + number
		if direction == SW and self.is_on_board((x - number, y + number)):
			return x - number, y + number

	def adjacent_tiles(self, pos: Coords) -> List[Coords]:
		return [self.squares_in_dir(pos, NE, 1),
		        self.squares_in_dir(pos, NW, 1),
		        self.squares_in_dir(pos, SE, 1),
		        self.squares_in_dir(pos, SW, 1)]

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
				if piece.color is BLUE:
					if self.matrix_coords(self.squares_in_dir(coords, NW, 1)).piece is None:
						normal_legal_moves.append(self.squares_in_dir(coords, NW, 1))
					if self.matrix_coords(self.squares_in_dir(coords, NE, 1)).piece is None:
						normal_legal_moves.append(self.squares_in_dir(coords, NE, 1))
				elif piece.color is RED:
					if self.matrix_coords(self.squares_in_dir(coords, SW, 1)).piece is None:
						normal_legal_moves.append(self.squares_in_dir(coords, SW, 1))
					if self.matrix_coords(self.squares_in_dir(coords, SE, 1)).piece is None:
						normal_legal_moves.append(self.squares_in_dir(coords, SE, 1))

		return normal_legal_moves

	# TODO: highlight legal moves
	def legal_moves(self, coords: Coords) -> List[Coords]:
		legal_moves = list()
		legal_moves.extend(self.move_possible_squares(coords))
		legal_moves.extend(self.hop_possible_squares(coords))

		return legal_moves

	# TODO: hop possible squares for king
	def hop_possible_squares(self, coords: Coords) -> List[Coords]:
		hop_moves = []
		(x, y) = coords
		piece: Piece = self.matrix[x][y].piece

		if piece is not None:
			if piece.king is False:
				for move in self.adjacent_tiles(coords):
					if move is not None and self.is_on_board(move):
						# If on adjacent tile there is an enemy
						if self.matrix_coords(move).piece is not None and self.matrix_coords(
								move).piece.color != self.matrix_coords(coords).piece.color:
							# Position one behind enemy
							pos_behind = (move[0] + (move[0] - coords[0]), move[1] + (move[1] - coords[1]))
							if self.is_on_board(pos_behind) and self.matrix_coords(pos_behind).piece is None:
								hop_moves.append(pos_behind)
		return hop_moves


class Square:
	def __init__(self, color: Color, location: Coords, piece=None):
		self.color: Color = color
		self.piece: 'Piece' = piece
		self.location: Coords = location
		self.highlighted: bool = False


class Piece:
	def __init__(self, color: Color, king=False):
		self.color: Color = color
		self.king: bool = king
