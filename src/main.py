import pygame

screen_size = 600
square_size = int(screen_size/8)
piece_size = int(square_size/2)
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
BLUE = (0,0,255)

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
		self.bg = pygame.image.load('img/board.png').convert()
		self.bg_rect = self.bg.get_rect()

	def setup_window(self):
		pygame.init()
		pygame.display.set_caption('Checkers!')
		self.generateBg()

	def generateBg(self):
		self.screen.fill((255, 255, 255))
		self.screen.blit(self.bg, self.bg_rect)

	def updateScreen(self, board):
		self.generateBg()
		
		#tutaj dodawać funkcje rysujące na ekran
				
		pygame.display.update()
		self.clock.tick(self.fps)
		
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

class Piece:
	def __init__(self, color, king = False):
		self.color = color
		self.king = king

class Square:
	def __init__(self, color, piece = None):
		self.color = color
		self.piece = piece
		
def main():
	game = Game()
	game.main()
if __name__ == "__main__":
	main()