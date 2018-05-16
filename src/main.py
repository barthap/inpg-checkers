import pygame

screen_size = 600
square_size = int(screen_size/8)
piece_size = int(square_size/2)
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
RED =   (255,   0,   0)
BLUE =  (  0,  0,  255)

class Game:
	def __init__(self):
		self.graphics = Graphics()
		self.board = Board()

	def main(self):
		self.setup()

		while True:
			self.gameLoop()
			self.updateGame()

	def setup(self):
		self.graphics.setup_window()

	def quit(self):
		pygame.quit()
		quit()

	def updateGame(self):
		self.graphics.updateScreen(self.board)

	def gameLoop(self):
	#główna pętla gry - tutaj się dzieje cała magia
	
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.quit()
				
class Graphics:
	def __init__(self):
		self.screen = pygame.display.set_mode((screen_size, screen_size))
		self.clock = pygame.time.Clock()
		self.fps = 60
		self.bg = pygame.image.load('img/board.png')
		self.bg_rect = self.bg.get_rect()
		self.redpiece = pygame.image.load('img/redpiece.png')
		self.bluepiece = pygame.image.load('img/bluepiece.png')
		self.blueking = pygame.image.load('img/blueking.png')
		self.redking = pygame.image.load('img/redking.png')

	def setup_window(self):
		pygame.init()
		pygame.display.set_caption('Checkers!')
		self.generateBg()

	def generateBg(self):
		self.screen.fill((255, 255, 255))
		self.screen.blit(self.bg, self.bg_rect)

	def updateScreen(self, board):
		self.generateBg()
		self.draw_board_pieces(board)
		#tutaj dodawać funkcje rysujące na ekran
				
		pygame.display.update()
		self.clock.tick(self.fps)

	def draw_board_pieces(self, board):
		for x in range(8):
			for y in range(8):
				if board.coordRename((x,y)).piece != None:
					if board.coordRename((x, y)).piece.color == RED and board.coordRename((x, y)).piece.king == False:
						self.screen.blit(self.redpiece, whatPixel((x,y)))
					elif board.coordRename((x, y)).piece.color == RED and board.coordRename((x, y)).piece.king == True:
						self.screen.blit(self.redking, whatPixel((x, y)))
					elif board.coordRename((x, y)).piece.color == BLUE and board.coordRename((x, y)).piece.king == True:
						self.screen.blit(self.blueking, whatPixel((x, y)))
					elif board.coordRename((x, y)).piece.color == BLUE and board.coordRename((x, y)).piece.king == False:
						self.screen.blit(self.bluepiece, whatPixel((x, y)))


def whatPixel(board_coords):
	#zwraca górny lewy pixel danego pola planszy
		return board_coords[0] * square_size , board_coords[1] * square_size


def whatSquare(pixel_coord):
		return int(pixel_coord[0] / square_size), int(pixel_coord[2] / square_size)


class Board:
	def __init__(self):
		self.matrix = self.generateBoard()


	def coordRename(self, coords):
		return self.matrix[coords[0]][coords[1]]


	def generateBoard(self):
		boardMatrix = [[None] * 8 for i in range (8)]

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
	def __init__(self, color, piece = None):
		self.color = color
		self.piece = piece


class Piece:
	def __init__(self, color, king = False):
		self.color = color
		self.king = king


def main():
	game = Game()
	game.main()


if __name__ == "__main__":
	main()