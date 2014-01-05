from components import matrix_config

MAX_LIVES = 3


class Player(object):
    """
    """
    def __init__(self, start_lane):
        self.speed = 4  # y - location, between 0 to 8 on the board
        self.lane = start_lane  # x - between 0-3
        self.life = MAX_LIVES  # means how many blocks we can handle
        self.action = matrix_config.ACTIONS[0]
