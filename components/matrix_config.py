# Matrix configuration
HEIGHT = 9
WIDTH = 4
NUMBER_OF_OBSTACLES = 15
NUMBER_OF_PLAYERS = 4
ROW_HEIGHT = 65
CELL_WIDTH = 130
LEFT_MARGIN = 95
TOP_MARGIN = 10

OBSTACLES_GLOB = 'client/res/obstacles/obstacle*.png'
ROAD_GLOB = 'client/res/bg/bg*.png'

# Obstacles
EMPTY = -1
OBSTACLES = {'CRACK': 0,
             'TRASH': 1,
             'PENGIUN': 2,
             'BIKE': 3,
             'WATER': 4,
             'BARRIER': 5}

ACTIONS = {'RIGHT': 1,
           'LEFT': 2,
           'PICKUP': 3,
           'JUMP': 4,
           'BRAKE': 5}

OBSTACLES_FOR_NEXT_ROW = OBSTACLES
OBSTACLES_FOR_NEXT_ROW['EMPTY'] = EMPTY

# Gamer lives
NUM_OF_LIVES = 3

SCORE = {'CRACK': ({'JUMP': 0}, -1),
         'TRASH': ({}, -1),
         'PENGUIN': ({'PICK': 1}, 0),
         'BIKE': ({}, -1),
         'WATER': ({'BRAKE'}, -1),
         'BARRIER': ({}, -1)}