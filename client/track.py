import glob
import pygame
from components import component
from common import config, obstacles


class Track(component.Component):

    def __init__(self):
        self._matrix = [[obstacles.NONE] * config.matrix_width
                        for x in range(config.matrix_height)]
        self._road_textures = None
        self._obstacle_textures = None

    # Component interface

    def init(self):
        # Note: road texture files must be sorted to avoid horizontal seems
        # between images.
        self._road_textures = [pygame.image.load(path) for path in
                               sorted(glob.glob(config.road_glob))]
        self._obstacle_textures = [pygame.image.load(path) for path in
                                   glob.glob(config.obstacles_glob)]

    def update(self, info):
        self._matrix = info['track']

    def draw(self, surface):
        # draw road background:
        for i in range(config.matrix_height):
            surface.blit(self.road_textures[i % len(self.road_textures)],
                        (0, i * config.row_height))

        # Draw obstacles on top of road:
        for y, row in enumerate(self._matrix):
            for x, cell in enumerate(row):
                if cell != obstacles.NONE:
                    texture = self.obstacle_textures[cell]
                    coordinates = self._get_surface_coordinates(x, y)
                    surface.blit(texture, coordinates)

    # Track interface

    def get_obstacle(self, x, y):
        """ Return the obstacle in position x, y """
        return self._matrix[y][x]

    # Private

    def _get_surface_coordinates(self, x, y):
        """ Convert matrix coordinates to surface coordinates """
        surface_x = config.left_margin + x * config.cell_width
        surface_y = config.top_margin + y * config.row_height
        return surface_x, surface_y
