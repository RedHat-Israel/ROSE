# Matrix configuration
HEIGHT = 9
WIDTH = 4
NUMBER_OF_OBSTACLES = 15
NUMBER_OF_PLAYERS = 4
ROW_HEIGHT = 10

TILE_TEXTURE_FILES_DIR = 'res/obstacle_tiles'
ROAD_TEXTURE_FILES = 'res/road_textures'

# Obstacles
EMPTY = 0
OBSTACLES = {'WATER': 0,
             'SNOW': 1,
             'HOLE': 2,
             'WALL': 3,
             'OIL': 4,
             'NAILS': 5,
             'BUMPER': 6,}

MOVE = {'FORWARD': 0,
        'RIGHT': 1,
        'LEFT': 2}

ACTIONS = {'PICK': 0,
           'JUMP': 1,}

OBSTACLES_FOR_NEXT_ROW = OBSTACLES
OBSTACLES_FOR_NEXT_ROW['EMPTY'] = EMPTY
