import unittest
from typing import Tuple

from utils.constants import RED, BLUE, BLACK, SE, NE, NW, SW, WHITE
from game import Board, Piece, Square, SquareMatrix, Coords


# Utility functions
def setup_empty_matrix() -> SquareMatrix:
	empty_matrix = [[None]*8 for _ in range(8)]

	for x in range(8):
		for y in range(8):
			if (x, y) in Board.all_board_coords():
				empty_matrix[x][y] = Square(BLACK, (x, y))
			else:
				empty_matrix[x][y] = Square(WHITE, (x, y))

	return empty_matrix


def set_pieces(board: Board, pieces: Tuple[Coords, Piece]) -> None:
	for p in pieces:
		pos = p[0]
		piece = p[1]
		assert Board.is_on_board(pos)
		sq = board.matrix_coords(pos)
		assert sq is not None
		sq.piece = piece


def draw_ascii_board(board: Board) -> None:
	print("     ", end="", flush=False)
	for i in range(8):
		print(i, end="  |  ", flush=False)
	print("\n--+-----+-----+-----+-----+-----+-----+-----+-----+", flush=False)
	for x in range(8):
		print(x, end=" |  ", flush=False)
		for y in range(8):
			sq = board.matrix[y][x]
			if sq is not None and sq.piece is not None:
				piece = sq.piece
				if piece.king is True:
					print("BK" if piece.color is BLUE else "RK", end=" |  ", flush=False)
				else:
					print("B" if piece.color is BLUE else "R", end="  |  ", flush=False)
			else:
				print(" ", end="  |  ", flush=False)
		print("\n--+-----+-----+-----+-----+-----+-----+-----+-----+", flush=False)

	print("", flush=True)


class BoardTests(unittest.TestCase):
	def setUp(self):
		self.board = Board()
		self.board.matrix = setup_empty_matrix()

	def test_isMatrixEmpty(self):
		for x in range(8):
			for y in range(8):
				sq = self.board.matrix_coords((x, y))
				if sq is not None and sq.color == BLACK:
					self.assertIn((x, y), Board.all_board_coords())
					self.assertIsNone(sq.piece)
					self.assertEqual(sq.color, BLACK)
				else:
					self.assertNotIn((x, y), Board.all_board_coords())

	def test_adjacentTiles(self):
		coords = (3, 3)
		valid_adjacent = [(4, 4), (2, 2), (2, 4), (4, 2)]

		adjacent = self.board.adjacent_tiles(coords)

		for pos in valid_adjacent:
			self.assertIn(pos, adjacent)

	def test_squaresInDir(self):
		start_pos = (3, 3)
		dist = 3
		valid_ne = (6, 0)
		valid_se = (6, 6)
		valid_nw = (0, 0)
		valid_sw = (0, 6)

		self.assertEqual(self.board.squares_in_dir(start_pos, SE, dist), valid_se)
		self.assertEqual(self.board.squares_in_dir(start_pos, SW, dist), valid_sw)
		self.assertEqual(self.board.squares_in_dir(start_pos, NE, dist), valid_ne)
		self.assertEqual(self.board.squares_in_dir(start_pos, NW, dist), valid_nw)

	def test_isOnBoard(self):
		self.assertTrue(Board.is_on_board((0, 0)))
		self.assertTrue(Board.is_on_board((0, 7)))
		self.assertTrue(Board.is_on_board((7, 0)))
		self.assertTrue(Board.is_on_board((7, 7)))
		self.assertTrue(Board.is_on_board((4, 6)))

		self.assertFalse(Board.is_on_board((0, 8)))
		self.assertFalse(Board.is_on_board((-1, 0)))


class GameLogicTests(unittest.TestCase):
	def setUp(self):
		self.board = Board()
		self.board.matrix = setup_empty_matrix()

	def test_knightPossible(self):
		pieces = [((0, 0), Piece(RED, False)),
		          ((2, 0), Piece(BLUE, False)),
		          ((0, 2), Piece(RED, False)),
		          ((0, 6), Piece(RED, False)),
		          ((1, 7), Piece(RED, False)),
		          ((3, 7), Piece(BLUE, False))]
		set_pieces(self.board, pieces)
		print("Knight possible test before:")
		draw_ascii_board(self.board)

		self.board.knight_possible()
		print("After:")
		draw_ascii_board(self.board)

		self.assertFalse(self.board.matrix_coords((0, 0)).piece.king)
		self.assertTrue(self.board.matrix_coords((2, 0)).piece.king)
		self.assertFalse(self.board.matrix_coords((0, 2)).piece.king)
		self.assertFalse(self.board.matrix_coords((0, 6)).piece.king)
		self.assertTrue(self.board.matrix_coords((1, 7)).piece.king)
		self.assertFalse(self.board.matrix_coords((3, 7)).piece.king)


	def test_normalMove(self):
		blue_pos = (3, 5)
		red_pos = (5, 1)
		pieces = [(blue_pos, Piece(BLUE, False)),
		          (red_pos, Piece(RED, False))]
		set_pieces(self.board, pieces)
		print("Normal move test")
		draw_ascii_board(self.board)

		blue_legal = self.board.legal_moves(blue_pos)
		red_legal = self.board.legal_moves(red_pos)

		self.assertCountEqual(blue_legal, [(2, 4), (4, 4)])
		self.assertCountEqual(red_legal, [(4, 2), (6, 2)])

	def test_normalHop(self):
		tested_piece_pos = (4, 4)
		pieces = [((3, 5), Piece(BLUE, False)),
		          (tested_piece_pos, Piece(BLUE, False)),
		          ((5, 3), Piece(RED, False))]
		set_pieces(self.board, pieces)
		print("Hop move test")
		draw_ascii_board(self.board)

		self.assertListEqual(self.board.legal_moves(tested_piece_pos), [(6, 2)])

	def test_kingMove(self):
		tested_king_pos = (1, 1)
		pieces = [(tested_king_pos, Piece(RED, True)),
		          ((2, 0), Piece(RED, False)),
		          ((4, 4), Piece(RED, False))]
		set_pieces(self.board, pieces)
		print("King move test")
		draw_ascii_board(self.board)

		self.assertCountEqual(self.board.legal_moves(tested_king_pos), [(0, 0), (0, 2), (2, 2), (3, 3)])

	def test_kingHop_1(self):
		tested_king_pos = (1, 1)
		pieces = [(tested_king_pos, Piece(RED, True)),
		          ((2, 0), Piece(RED, False)),
		          ((3, 3), Piece(BLUE, False)),
		          ((6, 6), Piece(BLUE, False))]
		set_pieces(self.board, pieces)
		print("King hop test 1")
		draw_ascii_board(self.board)

		self.assertCountEqual(self.board.legal_moves(tested_king_pos), [(4, 4), (5, 5)])

	def test_kingHop_2(self):
		tested_king_pos = (1, 1)
		pieces = [(tested_king_pos, Piece(RED, True)),
		          ((2, 0), Piece(RED, False)),
		          ((3, 3), Piece(BLUE, False)),
		          ((4, 4), Piece(BLUE, False))]
		set_pieces(self.board, pieces)
		print("King hop test 2")
		draw_ascii_board(self.board)

		self.assertNotIn((5, 5), self.board.legal_moves(tested_king_pos))
		self.assertListEqual(self.board.hop_possible_squares(tested_king_pos), [])

	# Tests if reported issue is solved
	def test_kingHop_problem1(self):
		tested_king_pos = (4, 0)
		pieces = [(tested_king_pos, Piece(BLUE, True)),
		          ((5, 1), Piece(RED, False)),
		          ((3, 1), Piece(RED, False)),
		          ((2, 2), Piece(RED, False))]
		set_pieces(self.board, pieces)
		print("King hop test problem 1")
		draw_ascii_board(self.board)

		self.assertCountEqual(self.board.legal_moves(tested_king_pos), [(6, 2), (7, 3)])

	# Tests if reported issue is solved
	def test_kingHop_problem2(self):
		tested_king_pos = (1, 1)
		pieces = [(tested_king_pos, Piece(BLUE, True)),
		          ((4, 4), Piece(RED, False)),
		          ((7, 7), Piece(BLUE, False))]
		set_pieces(self.board, pieces)
		print("King hop test problem 2")
		draw_ascii_board(self.board)

		self.assertCountEqual(self.board.legal_moves(tested_king_pos), [(5, 5), (6, 6)])


if __name__ == "__main__":
	unittest.main()
