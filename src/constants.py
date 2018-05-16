
# Constants and settings used all over the app
# Constant names should be UPPER_CASE

# App general config
WINDOW_TITLE: str = "Checkers !"
SCREEN_SIZE = 600   # Window width and height

# Filesystem utility constants
RESOURCE_PATH = "resources"     # relative path to resource folder
IMAGE_PATH = "img"              # image folder name (inside resources)

# Constants used in gameplay
SQUARE_SIZE = int(SCREEN_SIZE / 8)
PIECE_SIZE = int(SQUARE_SIZE / 2)

# Color definitions
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)