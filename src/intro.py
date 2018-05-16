import pygame

from constants import *
from scene import BaseScene
from menu import MenuScene


# Scene for showing intro
# I created this intro just for demo purposes
class IntroScene(BaseScene):
    def __init__(self, app):
        super().__init__(app)
        self.img = app.resource_manager.get_image('intro.jpg')
        self.img = pygame.transform.scale(self.img, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.img_rect = self.img.get_rect()

    def setup(self):
        self.app.graphics.clear_screen()
        self.app.graphics.draw(self.img, self.img_rect)

        font = pygame.font.SysFont("comicsansms", 24)
        text = font.render("Wciśnij Enter lub Spację, aby rozpocząć", True, (0, 255, 0))

        # Set text coordinates
        text_x = SCREEN_WIDTH / 2 - text.get_width() // 2
        text_y = SCREEN_HEIGHT / 4 - text.get_height() // 2

        self.app.graphics.draw(text, (text_x, text_y))

    def update(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and (event.key == pygame.K_RETURN or event.key == pygame.K_SPACE):
                self.app.switch_state(MenuScene(self.app))
