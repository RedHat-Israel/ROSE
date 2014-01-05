from components import matrix_config

MAX_LIVES = 3


class Player(object):
    """
    """
    def __init__(self, name, start_lane):
        self.name = name
        self.speed = 4  # y - location, between 0 to 8 on the board
        self.lane = start_lane  # x - between 0-3
        self.life = MAX_LIVES  # means how many blocks we can handle
        self.action = matrix_config.ACTIONS['NONE']

    def encode(self):
        """ Return representation as native type the can be serialized """
        return {'name': self.name,
                'speed': self.speed,
                'lane': self.lane,
                'life': self.life}

