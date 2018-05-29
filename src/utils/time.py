import pygame


class GameTimer:
	def __init__(self, start_offset=0):
		self.start_time = pygame.time.get_ticks() // 1000 - start_offset
		self.current_time = 0
		self.paused_time = 0
		self.is_paused = False

	def restart(self, offset=0):
		self.start_time = pygame.time.get_ticks() // 1000 - offset
		self.paused_time = 0

	def pause(self):
		self.paused_time = self.current_time
		self.is_paused = True

	def resume(self):
		self.paused_time = pygame.time.get_ticks() // 1000 - self.paused_time
		self.is_paused = False

	def get(self):
		self.current_time = pygame.time.get_ticks() // 1000 - self.start_time - self.paused_time
		return self.current_time
