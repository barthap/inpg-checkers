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

    def setup(self):
        pass

    def update(self, events):
        self.renderer.render_screen(self.board)


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
                if board.coordRename((x, y)).piece != None:
                    if board.coordRename((x, y)).piece.color == RED and board.coordRename((x, y)).piece.king == False:
                        self.graphics.draw(self.redpiece, whatPixel((x, y)))
                    elif board.coordRename((x, y)).piece.color == RED and board.coordRename((x, y)).piece.king == True:
                        self.graphics.draw(self.redking, whatPixel((x, y)))
                    elif board.coordRename((x, y)).piece.color == BLUE and board.coordRename((x, y)).piece.king == True:
                        self.graphics.draw(self.blueking, whatPixel((x, y)))
                    elif board.coordRename((x, y)).piece.color == BLUE and board.coordRename((x, y)).piece.king == False:
                        self.graphics.draw(self.bluepiece, whatPixel((x, y)))


def whatPixel(board_coords):
    # zwraca górny lewy pixel danego pola planszy
    return board_coords[0] * SQUARE_SIZE, board_coords[1] * SQUARE_SIZE


def whatSquare(pixel_coord):
    return int(pixel_coord[0] / SQUARE_SIZE), int(pixel_coord[2] / SQUARE_SIZE)


class Board:
    def __init__(self):
        self.matrix = self.generateBoard()

    def coordRename(self, coords):
        return self.matrix[coords[0]][coords[1]]

    def generateBoard(self):
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

        for x in range(8):
            for y in range(3):
                if boardMatrix[x][y].color == BLACK:
                    boardMatrix[x][y].piece = Piece(RED)
            for y in range(5, 8):
                if boardMatrix[x][y].color == BLACK:
                    boardMatrix[x][y].piece = Piece(BLUE)

        return boardMatrix


class Square:
    def __init__(self, color, piece=None):
        self.color = color
        self.piece = piece


class Piece:
    def __init__(self, color, king=False):
        self.color = color
        self.king = king
