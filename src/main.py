import pygame

screen_size = 600

class Graphics:
	def __init__(self):
		self.screen = pygame.display.set_mode((screen_size, screen_size))
		pygame.display.set_caption('Checkers!')
		self.clock = pygame.time.Clock()
		self.bg = pygame.image.load('img/board.png').convert()
		self.bg_rect = self.bg.get_rect()

pygame.init()
game = Graphics()
Window = pygame.display.set_mode((screen_size, screen_size))
pygame.display.set_caption('Checkers!')
clock = pygame.time.Clock()

gameRunning = True
while gameRunning:
	Window.fill((255, 255, 255))
	Window.blit(game.bg, game.bg_rect)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			gameRunning = False

	pygame.display.flip()

pygame.quit()
quit()
