
import random

import config


class Matrix():
    def __init__(self):
        self.matrix = [[config.EMPTY for x in xrange(config.WIDTH)]
                       for x in xrange(config.HEIGHT)]

    def generate_obstacles(self):
        for i in range(config.WIDTH):
            for j in range(1, config.NUMBER_OF_OBSTACLES + 1):
                _rand = random.randint(0, config.HEIGHT - 1)
                _obst = random.choice(config.OBSTACLES.values())
                self.matrix[_rand][i] = _obst

    def print_matrix(self):
        for i in self.matrix:
            print i
