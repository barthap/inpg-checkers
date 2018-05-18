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
        self.hopped = False     # Have just hopped in last turn

    def select_piece(self):
        mouse_square: Square = self.mouse_in_what_square()  # just make a variable once
        if mouse_square.piece is not None and mouse_square.piece.color == self.turn:
            # Somebody else can hop but not me:
            if self.can_anyone_hop() and not self.can_hop(mouse_square.location):
                print("Other piece can HOP!")
                return
            self.update_selected(mouse_square)

    def update_selected(self, new_square: 'Square', end_if_no_legal=False):
        self.selected_square = new_square
        self.selected_square.highlighted = True
        print("selected", self.selected_square.location)

        legal_moves = self.board.legal_moves(self.selected_square.location)
        if len(legal_moves) > 0:
            print('legal:')
            for location in legal_moves:
                print(location)
                self.board.matrix_coords(location).highlighted = True
        else:
            print('no legal moves')
            self.deselect_piece()
            if end_if_no_legal is True:
                self.switch_turn()

    def deselect_piece(self):
        self.board.remove_all_highlights()
        self.selected_square = None
        print("unselected")

    def move_piece(self):
        mouse_square = self.mouse_in_what_square()
        if self.selected_square is not None:
            if mouse_square == self.selected_square and not self.can_hop() and not self.hopped:
                print('same, deselecting')
                self.deselect_piece()

            if mouse_square.color is BLACK and mouse_square.piece is None:
                if mouse_square.location in self.board.legal_moves(self.selected_square.location):
                    if self.can_hop():  # Hop an enemy
                        enemy_pos = self.board.position_between(self.selected_square.location, mouse_square.location)
                        enemy_piece = self.board.matrix_coords(enemy_pos)
                        print("HOPPED AN ENEMY!")
                        self.hopped = True
                        self.board.remove_piece(enemy_piece)    # Remove an enemy
                        self.board.remove_all_highlights()      # Remove old highlights
                        mouse_square.piece = self.selected_square.piece
                        self.board.remove_piece(self.selected_square)
                        self.update_selected(mouse_square, True)      # Piece is selected at its new position
                    else:
                        mouse_square.piece = self.selected_square.piece
                        self.board.remove_piece(self.selected_square)
                        self.deselect_piece()
                        self.switch_turn()
                        self.hopped = False

    # If location argument is empty, it checks currently selected_square
    def can_hop(self, location: Coords=None) -> bool:
        if location is None:
            if self.selected_square is None:
                return False
            location = self.selected_square.location

        adj = self.board.adjacent_tiles(location)
        for move in self.board.legal_moves(location):
            if move not in adj:
                return True
        return False

    # Can anyone hop in this turn
    def can_anyone_hop(self):
        for x in range(8):
            for y in range(8):
                sq = self.board.matrix_coords((x,y))
                if sq.piece is not None and sq.piece.color == self.turn:
                    if self.can_hop((x,y)):
                        return True
        return False

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

    def remove_all_highlights(self) -> None:
        for x in range(8):
            for y in range(8):
                self.matrix[x][y].highlighted = False

    # Used for finding enemy position when hopping
    @staticmethod
    def position_between(pos_a: Coords, pos_b: Coords):
        enemy_pos_x = int(pos_a[0] + (pos_b[0] - pos_a[0]) / 2)
        enemy_pos_y = int(pos_a[1] + (pos_b[1] - pos_a[1]) / 2)
        enemy_pos = (enemy_pos_x, enemy_pos_y)
        return enemy_pos

    # Returns coordinates of tile relative ('number' fields away) to a position in specified direction
    # DOES NOT CHECK IF ON BOARD!
    def squares_in_dir(self, position: Coords, direction, number: int = 1) -> Coords:
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
    def adjacent_tiles(self, pos: Coords) -> List[Coords]:
        return [self.squares_in_dir(pos, NE),
                self.squares_in_dir(pos, NW),
                self.squares_in_dir(pos, SE),
                self.squares_in_dir(pos, SW)]

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
                    nw_dir = self.squares_in_dir(coords, NW, 1)
                    if self.is_on_board(nw_dir) and self.matrix_coords(nw_dir).piece is None:
                        normal_legal_moves.append(nw_dir)

                    ne_dir = self.squares_in_dir(coords, NE, 1)
                    if self.is_on_board(ne_dir) and self.matrix_coords(ne_dir).piece is None:
                        normal_legal_moves.append(ne_dir)
                elif piece.color is RED:
                    sw_dir = self.squares_in_dir(coords, SW, 1)
                    if self.is_on_board(sw_dir) and self.matrix_coords(sw_dir).piece is None:
                        normal_legal_moves.append(sw_dir)

                    se_dir = self.squares_in_dir(coords, SE, 1)
                    if self.is_on_board(se_dir) and self.matrix_coords(se_dir).piece is None:
                        normal_legal_moves.append(se_dir)

        return normal_legal_moves

    def legal_moves(self, coords: Coords) -> List[Coords]:
        legal_moves = list()
        legal_moves.extend(self.move_possible_squares(coords))
        hop_moves = self.hop_possible_squares(coords)
        if len(hop_moves) > 0:
            legal_moves = hop_moves

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
