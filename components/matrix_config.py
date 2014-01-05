# Matrix configuration

HEIGHT = 9
WIDTH = 4
ROW_HEIGHT = 65
CELL_WIDTH = 130
LEFT_MARGIN = 95
TOP_MARGIN = 10
MAX_OBSTACLES = 15
OBSTACLES_GLOB = 'client/res/obstacles/obstacle*.png'
ROAD_GLOB = 'client/res/bg/bg*.png'
EMPTY = -1
OBSTACLES = CRACK, TRASH, PENGIUN, BIKE, WATER, BARRIER = tuple(range(6))

# Player

MAX_LIVES = 3
MAX_PLAYERS = 4
ACTIONS = NONE, RIGHT, LEFT, PICKUP, JUMP, BRAKE = tuple(range(6))
