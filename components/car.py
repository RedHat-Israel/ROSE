import pygame
import matrix_config
import os
import config
from components import component

class Car(component.Component):

    def __init__(self, id, lane, speed):
        self.id = id
        self.lane = lane
        self.speed = speed
        self.texture = None

    def init(self):
        path = os.path.join(config.cars_dir, 'car%d.png' % self.id)
        self.texture = pygame.image.load(path)

    def update(self, info):
        self.lane = info['lane']
        self.speed = info['speed']

    def draw(self, surface):
        x = matrix_config.LEFT_MARGIN + self.lane * matrix_config.CELL_WIDTH
        y = self.speed * matrix_config.ROW_HEIGHT
        surface.blit(self.texture, (x, y))
