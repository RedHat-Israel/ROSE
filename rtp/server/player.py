from rtp.common import actions, config


class Player(object):

    def __init__(self, name, car):
        self.name = name
        self.car = car
        self.speed = None
        self.lane = None
        self.action = None
        self.response_time = None
        self.reset()

    # Game state interface

    def update(self):
        """ Go to the next game state """

    def reset(self):
        self.speed = 6   # y - location, between 0 to 8 on the board
        self.lane = self.car  # x - between 0-3
        self.action = actions.NONE
        self.response_time = 1.0

    def state(self):
        """ Return read only serialize-able state for sending to client """
        return {'name': self.name,
                'car': self.car,
                'speed': self.speed,
                'lane': self.lane}
