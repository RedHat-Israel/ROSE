from rtp.common import actions, config


class Player(object):

    def __init__(self, name, car):
        self.name = name
        self.car = car
        self.position = None
        self.action = None
        self.response_time = None
        self.life = None
        self.reset()

    # Game state interface

    def update(self):
        """ Go to the next game state """

    def reset(self):
        # x - between 0-3
        # y - location, between 0 to 8 on the board
        self.position = [self.car, 6]
        self.action = actions.NONE
        self.response_time = 1.0
        self.life = 0

    def __cmp__(self, other):
        return cmp((self.position[1], -self.life), (other.position[1], -other.life))

    def state(self):
        """ Return read only serialize-able state for sending to client """
        return {'name': self.name,
                'car': self.car,
                'position': self.position,
                'life': self.life}
