import pygame
import matrix_config
import os
import config
from components import component

class Car(component.Component):

    def __init__(self, id, x, y):
        self.id = id
        self._location = (x, y)
        self.texture = None

    def init(self):
        path = os.path.join(config.cars_dir, 'car%d.png' % self.id)
        self.texture = pygame.image.load(path)

    def update(self, info):
        pass

    def draw(self, surface):
        x = matrix_config.LEFT_MARGIN + self._location[0] * matrix_config.CELL_WIDTH
        y = self._location[1] * matrix_config.ROW_HEIGHT
        surface.blit( self.texture, (x, y))
