from rtp.common import actions, config, core


class Player(object):

    def __init__(self, name, car, lane):
        self.name = name
        self.car = car
        self.lane = lane
        self.position = None
        self.action = None
        self.response_time = None
        self.life = None
        self.reset()

    # Game state interface

    def update(self):
        """ Go to the next game state """

    def reset(self):
        # x: | |0| | |1 | |
        # y: 2 / 3 of the track
        self.position = core.Point(self.lane * 3 + 1,
                                   config.matrix_height / 3 * 2)
        self.action = actions.NONE
        self.response_time = 1.0
        self.life = 0

    def __cmp__(self, other):
        return cmp((self.position.y, -self.life), (other.position.y, -other.life))

    def state(self):
        """ Return read only serialize-able state for sending to client """
        return {'name': self.name,
                'car': self.car,
                'position': [self.position.x, self.position.y],
                'lane': self.lane,
                'life': self.life}
