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
		self.graphics.updateScreen()

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

	def updateScreen(self):
		self.generateBg()
		
		#tutaj dodawać funkcje rysujące na ekran
				
		pygame.display.update()
		self.clock.tick(self.fps)
		
def main():
	game = Game()
	game.main()
if __name__ == "__main__":
	main()