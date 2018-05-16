import pygame
import pygameMenu                # This imports classes and other things
from pygameMenu.locals import *  # Import constants (like actions)

from constants import *
from scene import BaseScene
from game import GameScene


# Main Menu scene
class MenuScene(BaseScene):
    def __init__(self, app):
        super().__init__(app)

        # Main Menu
        self.menu = pygameMenu.Menu(app.graphics.screen, window_width=SCREEN_SIZE, window_height=SCREEN_SIZE,
                               font=pygameMenu.fonts.FONT_NEVIS,
                               title='Menu Gry', bgfun=None, dopause=False)

        # Show the rules
        self.help_menu = pygameMenu.TextMenu(app.graphics.screen, window_width=SCREEN_SIZE, window_height=SCREEN_SIZE,
                                        font=pygameMenu.fonts.FONT_FRANCHISE,
                                        onclose=PYGAME_MENU_DISABLE_CLOSE,
                                        title='Help', dopause=False,
                                        menu_color_title=(120, 45, 30),
                                        menu_color=(30, 50, 107))

    def setup(self):
        self.app.graphics.clear_screen()

        self.menu.add_option('Play', self.__go_play)  #TODO: Add timer submenu
        self.menu.add_option('Rules', self.help_menu)
        self.menu.add_option('Exit', self.app.exit)


		#TODO: Help menu
        HELP = ['To jest w pliku menu.py',
                'TODO: Dodac tu zasady z Rules.txt',
                'I jakies instrukcje poruszania sie',
                'Np kliknij myszka na pionek, potem na pole']

        for line in HELP:
            self.help_menu.add_line(line)  # Add line
        self.help_menu.add_option('Return to Menu', PYGAME_MENU_BACK)  # Add option

    def update(self, events):
        self.menu.mainloop(events)

    def __go_play(self):
        self.app.switch_state(GameScene(self.app))