import random
import glob
import pygame
from components import component
from common import config, obstacles


class Track(component.Component):

    def __init__(self):
        self.matrix = [[obstacles.NONE] * config.matrix_width
                       for x in range(config.matrix_height)]
        self.road_textures = None
        self.obstacle_textures = None

    # Component interface

    def init(self):
        # Note: road texture files must be sorted to avoid horizontal seems
        # between images.
        self.road_textures = [pygame.image.load(path) for path in
                              sorted(glob.glob(config.road_glob))]
        self.obstacle_textures = [pygame.image.load(path) for path in
                                  glob.glob(config.obstacles_glob)]

    def update(self, info):
        self.road_textures.insert(0, self.road_textures.pop())
        if 'track' in info:
            self.matrix = info['track']

    def draw(self, surface):
        # draw road background:
        for i in range(config.matrix_height):
            surface.blit(self.road_textures[i % len(self.road_textures)],
                        (0, i * config.row_height))

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
        cell = random.randrange(config.matrix_width)
        row = [obstacles.NONE] * config.matrix_width
        row[cell] = obstacles.get_random_obstacle()
        return row

    def advance(self):
        row = self.generate_row()
        self.matrix.pop()
        self.matrix.insert(0, row)

    def get_surface_coordinates(self, x, y):
        surface_x = config.left_margin + x * config.cell_width
        surface_y = config.top_margin + y * config.row_height
        return surface_x, surface_y


if __name__ == '__main__':
    m = Track()
    m.generate_obstacles()
    m.print_matrix()
