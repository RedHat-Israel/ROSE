import random

import config


class Matrix():
    def __init__(self):
        self.matrix = [[config.EMPTY for x in xrange(config.WIDTH)]
                       for x in xrange(config.HEIGHT)]

    def generate_obstacles(self):
        obstacles = 0
        while obstacles < config.NUMBER_OF_OBSTACLES:
            x = random.randint(0, config.WIDTH - 1)
            y = random.randint(0, config.HEIGHT - 1)

            if self.is_legal_obstacle_placement(x,y):
                self.matrix[y][x] = random.choice(config.OBSTACLES.values())
                obstacles += 1

    def is_legal_obstacle_placement(self, x, y):
        if y == 0:
            return self.check_below(x, y)
        elif y == config.HEIGHT - 1:
            return self.check_above(x, y)
        else:
            return self.check_above(x, y) and self.check_below(x, y)

    def check_below(self, x, y):
        return self.matrix[y + 1][x] == config.EMPTY

    def check_above(self, x, y):
        return self.matrix[y - 1][x] == config.EMPTY


    def print_matrix(self):
        for i in self.matrix:
            print i

m = Matrix()
m.generate_obstacles()
m.print_matrix()