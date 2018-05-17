import pygame

from graphics import Graphics
from intro import IntroScene
from resources import ResourceManager


# Main App class, initializes game, runs main loops, handles events etc
class App:
    def __init__(self):
        self.graphics = Graphics()              # PyGame rendering/graphic utils
        self.resource_manager = ResourceManager()
        self.__running = True                   # Flag determines if main loop should still run
        self.state = IntroScene(self)           # Loads state machine

    # Main function, it is ran in main.py
    def main(self):
        self.__setup()

        # Main loop
        while self.__running is True:
            self.__main_loop()

        # Finish app when main loop is done
        self.__quit()

    def exit(self):
        self.__running = False   # Break main loop

    # Function to change states, etc Intro -> Menu, Menu -> Game etc.
    def switch_state(self, new_state):
        self.state.destroy()
        self.state = new_state
        self.state.setup()

    # Methods and attributes which names start with __ (double underscore) are Private

    # Init the app
    def __setup(self):
        print("Starting game...")
        self.graphics.setup_window()
        self.state.setup()

    # Main loop content
    def __main_loop(self):
        # Handle Events
        # TODO: Add in-game Event System
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.__quit()

        # Update current state (Feed it with events), then update the renderer
        self.state.update(events)
        self.graphics.update_screen()

    # Called when user exits game
    def __quit(self):
        print("Game finished, closing")
        pygame.quit()
        quit()





