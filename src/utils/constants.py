
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
FONT_TEXT = __fontdir.format("src/fonts", 'Slabo27px-Regular')
FONT_MENU = __fontdir.format("src/fonts", 'Raleway-ExtraBold')

LOREM_IPSUM="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc varius nulla vitae quam aliquet vehicula. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Nam molestie, libero auctor consequat sollicitudin, nulla erat tempus enim, quis placerat neque lacus convallis dolor. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Morbi luctus quam at arcu accumsan, quis maximus dolor ultricies. Nulla luctus tincidunt sem quis faucibus. Nam congue, augue eget lacinia vehicula, neque est auctor sapien, eget elementum tortor diam quis velit. Pellentesque in sapien maximus, sollicitudin elit non, ultricies justo. Integer ut orci eget nisl facilisis facilisis. Quisque sapien lacus, cursus vel accumsan sed, molestie a nulla. Maecenas ullamcorper sem ante, in tincidunt felis hendrerit ut. Pellentesque consequat augue et feugiat rutrum. Donec vitae tellus consequat, ornare urna vel, varius nisl."
