import random
import matrix_config
import glob
import pygame
from components import component


class Matrix(component.Component):

    def __init__(self):
        self.matrix = [[matrix_config.EMPTY] * matrix_config.WIDTH
                       for x in range(matrix_config.HEIGHT)]
        self.road_textures = None
        self.obstacle_textures = None
        self.__generate_obstacles()

    # Component interface

    def init(self):
        # Note: road texture files must be sorted to avoid horizontal seems
        # between images.
        self.road_textures = [pygame.image.load(path) for path in
                              sorted(glob.glob(matrix_config.ROAD_GLOB))]
        self.obstacle_textures = [pygame.image.load(path) for path in
                                  glob.glob(matrix_config.OBSTACLES_GLOB)]

    def update(self, info):
        self.road_textures.insert(0, self.road_textures.pop())
        if 'matrix' in info:
            self.matrix = info['matrix']

    def draw(self, surface):
        # draw road background:
        for i in range(matrix_config.HEIGHT):
            surface.blit(self.road_textures[i % len(self.road_textures)],
                        (0, i * matrix_config.ROW_HEIGHT))

        # Draw obstacles on top of road:
        for y, row in enumerate(self.matrix):
            for x, cell in enumerate(row):
                if cell != matrix_config.EMPTY:
                    texture = self.obstacle_textures[cell]
                    coordinates = self.get_surface_coordinates(x, y)
                    surface.blit(texture, coordinates)

    # Other stuff

    def encode(self):
        return self.matrix

    def __generate_obstacles(self):
        """
        Generates obstacles for __init__
        """
        obstacles = 0
        while obstacles < matrix_config.MAX_OBSTACLES:
            x = random.randint(0, matrix_config.WIDTH - 1)
            y = random.randint(0, matrix_config.HEIGHT - 1)

            if self.is_legal_obstacle_placement(x, y):
                self.matrix[y][x] = self.get_random_obstacle()
                obstacles += 1

    def is_legal_obstacle_placement(self, x, y):
        """
        Checks if x and y are legal
        """

        if y == 0:
            return self.check_below(x, y)
        elif y == matrix_config.HEIGHT - 1:
            return self.check_above(x, y)
        else:
            return self.check_above(x, y) and self.check_below(x, y)

    def check_below(self, x, y):
        return self.matrix[y + 1][x] == matrix_config.EMPTY

    def check_above(self, x, y):
        return self.matrix[y - 1][x] == matrix_config.EMPTY

    def check_right(self, x, y):
        return self.matrix[y][x+1] == matrix_config.EMPTY

    def check_left(self, x, y):
        return self.matrix[y][x-1] == matrix_config.EMPTY

    def print_matrix(self):
        for i in self.matrix:
            print i

    def get_obstacle(self, x, y):
        """
        Return the obstacle in location x, y
        """
        return self.matrix[y][x]

    def generate_row(self):
        """
        Generates new row with obstacle
        """

        _counter = 0
        _tmp_list = []
        for i in self.matrix[0]:
            if i == matrix_config.EMPTY:
                _tmp_list.append(self.get_random_obstacle())
            else:
                _tmp_list.insert(_counter, matrix_config.EMPTY)
            _counter += 1

        return _tmp_list

    def get_random_obstacle(self):
        return random.choice(matrix_config.OBSTACLES)

    def advance(self):
        row = self.generate_row()
        self.matrix.pop()
        self.matrix.insert(0, row)

    def get_surface_coordinates(self, x, y):
        surface_x = matrix_config.LEFT_MARGIN + x * matrix_config.CELL_WIDTH
        surface_y = matrix_config.TOP_MARGIN + y * matrix_config.ROW_HEIGHT
        return surface_x, surface_y


if __name__ == '__main__':
    m = Matrix()
    m.generate_obstacles()
    m.print_matrix()
