import random
from rtp.common import config, obstacles


class Track(object):

    def __init__(self):
        self._matrix = None
        self.reset()

    # Game state interface

    def update(self):
        """ Go to the next game state """
        self._matrix.pop()
        self._matrix.insert(0, self._generate_row())

    def state(self):
        """ Return read only serialize-able state for sending to client """
        return tuple(tuple(row) for row in self._matrix)

    # Track interface

    def get_obstacle(self, x, y):
        """ Return the obstacle in position x, y """
        return self._matrix[y][x]

    def clear(self, x, y):
        """ Clear obstacle in position x, y """
        self._matrix[y][x] = obstacles.NONE

    def reset(self):
        self._matrix = [[obstacles.NONE] * config.matrix_width
                        for x in range(config.matrix_height)]

    # Private

    def _generate_row(self):
        """ Generates new row with obstacles """
        cell = random.randrange(config.matrix_width)
        row = [obstacles.NONE] * config.matrix_width
        row[cell] = obstacles.get_random_obstacle()
        return row
