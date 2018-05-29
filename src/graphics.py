import pygame

from utils.constants import *


# Utility class for graphics settings
class Graphics:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.fps = 60

    def setup_window(self):
        pygame.init()
        pygame.display.set_caption(WINDOW_TITLE)
        self.clear_screen()

    def clear_screen(self, color=None):
        if color is None:
            color = BLACK
        self.screen.fill(color)

    def draw(self, *kwargs):
        self.screen.blit(*kwargs)

    def update_screen(self):
        pygame.display.update()
        self.clock.tick(self.fps)
