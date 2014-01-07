import random
import matrix_config
import glob
import pygame
from components import component
from common import obstacles, actions


class Matrix(component.Component):

    def __init__(self):
        self.matrix = [[obstacles.NONE] * matrix_config.WIDTH
                       for x in range(matrix_config.HEIGHT)]
        self.road_textures = None
        self.obstacle_textures = None

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
                if cell != obstacles.NONE:
                    texture = self.obstacle_textures[cell]
                    coordinates = self.get_surface_coordinates(x, y)
                    surface.blit(texture, coordinates)

    # Other stuff

    def encode(self):
        return self.matrix

    def get_obstacle(self, x, y):
        """
        Return the obstacle in location x, y
        """
        return self.matrix[y][x]

    def generate_row(self):
        """
        Generates new row with obstacle
        """
        cell = random.randrange(matrix_config.WIDTH)
        row = [obstacles.NONE] * matrix_config.WIDTH
        row[cell] = obstacles.get_random_obstacle()
        return row

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
