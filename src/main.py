import pygame

screen_size = 600

class Game:
	def __init__(self):
		self.screen = pygame.display.set_mode((screen_size, screen_size))
		pygame.display.set_caption('Checkers!')
		self.background = pygame.image.load('img/board.png')
		self.clock = pygame.time.Clock()


pygame.init()
game = Game()

endGame = False

while not endGame:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			endgame = True

pygame.quit()
quit()
