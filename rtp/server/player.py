from rtp.common import actions, config


class Player(object):

    def __init__(self, name, car, lane):
        self.name = name
        self.car = car
        self.lane = lane
        self.x = None
        self.y = None
        self.action = None
        self.response_time = None
        self.life = None
        self.reset()

    # Game state interface

    def update(self):
        """ Go to the next game state """

    def reset(self):
        self.x = self.lane * 3 + 1              # | |0| | |1 | |
        self.y = config.matrix_height / 3 * 2   # 1/3 of track
        self.action = actions.NONE
        self.response_time = 1.0
        self.life = 0

    def __cmp__(self, other):
        return cmp((self.y, -self.life), (other.y, -other.life))

    def state(self):
        """ Return read only serialize-able state for sending to client """
        return {'name': self.name,
                'car': self.car,
                'x': self.x,
                'y': self.y,
                'lane': self.lane,
                'life': self.life}
