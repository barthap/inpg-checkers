
# Constants and settings used all over the app
# Constant names should be UPPER_CASE

# App general config
WINDOW_TITLE: str = "Checkers !"

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Filesystem utility constants
RESOURCE_PATH = "resources"     # relative path to resource folder
IMAGE_PATH = "img"              # image folder name (inside resources)
SOUND_PATH = "sfx"
SAVE_PATH = "saves"

# Constants used in gameplay
BOARD_SIZE = 600   # Window width and height
SQUARE_SIZE = int(BOARD_SIZE / 8)
PIECE_SIZE = int(SQUARE_SIZE / 2)

# Color definitions
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
BROWN = (25, 0, 0)

# Move directions definitions
NW = 'northwest'
NE = 'northeast'
SE = 'southeast'
SW = 'southwest'

# Scene names
# SCENE = 'filename.ClassName'
INTRO = 'intro.IntroScene'
MENU = 'menu.MenuScene'
GAME = 'game.GameScene'
PAUSE = 'pause.PauseScene'
END_GAME = 'endgame.EndGameScene'

# Config file names
CONFIG_FILE = 'config.ini'
LOCALE_FILE = 'locale.ini'

# Fonts
__fontdir = "{0}/{1}.ttf"
FONT_TEXT = __fontdir.format("resources/fonts", 'Slabo27px-Regular')
FONT_MENU = __fontdir.format("resources/fonts", 'Raleway-ExtraBold')

LOREM_IPSUM = "Go home Textmenu, You`re drunk."
