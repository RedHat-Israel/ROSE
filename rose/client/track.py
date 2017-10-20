import glob
import os
import pygame
from rose.common import config, obstacles
from .component import Component


class Track(Component):

    def __init__(self):
        self._track = {}
        self._road_textures = None
        self._obstacle_textures = None

    # Component interface

    def init(self):
        # Note: all texture files must be sorted by file name to get the
        # texture in the correct order.
        self._road_textures = [pygame.image.load(path) for path in
                               sorted(glob.glob(config.road_glob))]
        self._obstacle_textures = {}
        for name in obstacles.ALL[1:]:
            path = os.path.join(config.obstacles_dir, name + ".png")
            self._obstacle_textures[name] = pygame.image.load(path)

    def update(self, info):
        self._track = {(obs["x"], obs["y"]): obs["name"] for obs in info["track"]}
        if info['started']:
            # Simulate track movement
            last = self._road_textures.pop()
            self._road_textures.insert(0, last)

    def draw(self, surface):
        # draw road background:
        for i in range(config.matrix_height):
            surface.blit(self._road_textures[i % len(self._road_textures)],
                        (0, config.dashboard_height + (i * config.row_height)))

        # Draw obstacles on top of road:
        for (x, y), obs in self._track.iteritems():
            texture = self._obstacle_textures[obs]
            coordinates = self._get_surface_coordinates(x, y)
            surface.blit(texture, coordinates)

    # Track interface

    def get(self, x, y):
        """ Return the obstacle in position x, y """
        self._validate_pos(x, y)
        return self._track.get((x, y), obstacles.NONE)

    # Private

    def _validate_pos(self, x, y):
        if x < 0 or x > config.matrix_width - 1:
            raise IndexError('x out of range: 0-%d', config.matrix_width - 1)
        if y < 0 or y > config.matrix_height - 1:
            raise IndexError('y out of range: 0-%d', config.matrix_height - 1)

    def _get_surface_coordinates(self, x, y):
        """ Convert matrix coordinates to surface coordinates """
        surface_x = config.left_margin + x * config.cell_width
        surface_y = config.dashboard_height + config.top_margin + y * config.row_height
        return surface_x, surface_y
