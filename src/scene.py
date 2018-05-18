

# Base class for game scene (Intro, Menu, Game etc.). All states should derive from it
# TODO: Make it abstract
class BaseScene:
    def __init__(self, app: 'App'):
        self.app = app

    def setup(self):
        pass

    def update(self, events):
        pass

    # something like destructor, called when state is changing or app is quitting
    def destroy(self):
        pass
