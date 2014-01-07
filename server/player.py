from components import matrix_config
from common import actions

MAX_LIVES = 3


class Player(object):
    """
    """
    def __init__(self, name, car):
        self.name = name
        self.car = car
        self.speed = 4  # y - location, between 0 to 8 on the board
        self.lane = car  # x - between 0-3
        self.life = MAX_LIVES  # means how many blocks we can handle
        self.action = actions.NONE

    def encode(self):
        """ Return representation as native type the can be serialized """
        return {'name': self.name,
                'car': self.car,
                'speed': self.speed,
                'lane': self.lane,
                'life': self.life}

