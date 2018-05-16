import pygame

from resources import ResourceManager
from scene import BaseScene
from constants import *
from graphics import Graphics


# Main Game code
class GameScene(BaseScene):
	def __init__(self, app):
		super().__init__(app)
		self.renderer = GameRenderer(app.graphics, app.resource_manager)
		self.board = Board()
		self.turn = BLUE
		self.selected_square = None  # Board square

	def select_piece(self):
		if mouse_in_what_square(self).piece is not None and mouse_in_what_square(self).piece.color == self.turn:
				self.selected_square = mouse_in_what_square(self)

	def move_piece(self):
		if self.selected_square is not None and mouse_in_what_square(self).piece is None:
			if mouse_in_what_square(self) != self.selected_square:
				mouse_in_what_square(self).piece = self.selected_square.piece
				self.remove_piece(self.selected_square)

	def remove_piece(self, coords):
		coords.piece = None

	def setup(self):
		pass

	def update(self, events):
		self.renderer.render_screen(self.board)
		for event in events:
			if event.type == pygame.MOUSEBUTTONDOWN:
				if self.selected_square is None:
					self.select_piece()
				else:
					self.move_piece()

#TODO: czemu pozwala tylko raz przesunąć? - czy remove_piece None'uje self.selected_square?
#TODO: zmiana tury
#TODO: sprawdź bicie
#TODO: podświetl

class GameRenderer:
	def __init__(self, graphics: Graphics, resource_manager: ResourceManager):
		self.graphics = graphics
		self.bg = resource_manager.get_image('board.png')
		self.bg_rect = self.bg.get_rect()
		self.redpiece = resource_manager.get_image('redpiece.png')
		self.bluepiece = resource_manager.get_image('bluepiece.png')
		self.blueking = resource_manager.get_image('blueking.png')
		self.redking = resource_manager.get_image('redking.png')

	def generate_bg(self):
		self.graphics.clear_screen()
		self.graphics.draw(self.bg, self.bg_rect)

	def render_screen(self, board):
		self.generate_bg()
		self.draw_board_pieces(board)
		# tutaj dodawać funkcje rysujące na ekran

	def draw_board_pieces(self, board):
		for x in range(8):
			for y in range(8):
				if board.matrix_coords((x, y)).piece != None:
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


def what_pixel(board_coords):
	# zwraca górny lewy pixel danego pola planszy
	return board_coords[0] * SQUARE_SIZE, board_coords[1] * SQUARE_SIZE


def what_square(pixel_coord):
	return int(pixel_coord[0] / SQUARE_SIZE), int(pixel_coord[1] / SQUARE_SIZE)


def mouse_in_what_square(GameScene):
	return GameScene.board.matrix_coords(what_square(pygame.mouse.get_pos()))


class Board:
	def __init__(self):
		self.matrix = self.generate_board_matrix()

	def matrix_coords(self, coords):
		return self.matrix[coords[0]][coords[1]]

	def generate_board_matrix(self):
		boardMatrix = [[None] * 8 for i in range(8)]

		for x in range(8):
			for y in range(8):
				if (x % 2 != 0) and (y % 2 == 0):
					boardMatrix[y][x] = Square(WHITE)
				elif (x % 2 != 0) and (y % 2 != 0):
					boardMatrix[y][x] = Square(BLACK)
				elif (x % 2 == 0) and (y % 2 != 0):
					boardMatrix[y][x] = Square(WHITE)
				elif (x % 2 == 0) and (y % 2 == 0):
					boardMatrix[y][x] = Square(BLACK)

		# tutaj zmieniać, jeżeli w opcjach zostanie zmieniony wariant gry pomięddzy 2-3 rzędy
		for x in range(8):
			for y in range(3):
				if boardMatrix[x][y].color == BLACK:
					boardMatrix[x][y].piece = Piece(RED)
			for y in range(5, 8):
				if boardMatrix[x][y].color == BLACK:
					boardMatrix[x][y].piece = Piece(BLUE)

		return boardMatrix

	def tile_adjacent(self, positon, direcion):
		if direcion == NW:
			return (positon[0] - 1, positon[1] - 1)
		if direcion == NE:
			return (positon[0] - 1, positon[1] + 1)
		if direcion == SE:
			return (positon[0] + 1, positon[1] - 1)
		if direcion == SW:
			return (positon[0] + 1, positon[1] + 1)


class Square:
	def __init__(self, color, piece=None):
		self.color = color
		self.piece = piece


class Piece:
	def __init__(self, color, king=False):
		self.color = color
		self.king = king
