#General
FPS = 60
GAME_SQUARE = 4
DEBUGGING = True

#WINDOW settings
MARGIN = 200
CELL_SIZE = 120
WIDTH = GAME_SQUARE * CELL_SIZE
HEIGHT = WIDTH + MARGIN
TITLE = "2048"

#Color Palette
#BG_COLOR = (26, 217, 169)
BLACK = (0, 0, 0)
WHITE = (230, 230, 230)
BG_COLOR = (204, 197, 184)
LINE_COLOR = (153, 147, 138)
COLORS = {
    2 : (150, 226, 255),
    4 : (0, 247, 255),
    8 : (12, 199, 232),
    16: (0, 167, 235),
    32: (12, 134, 235),
    64: (4, 91, 255),
    128 : (130, 255, 158),
    256 : (0, 255, 88),
    512 : (0, 250, 37),
    1024: (13, 230, 0),
    2048: (64, 217, 0),
    4096: (80, 148, 25)
}
