import random
import pygame
import os
from common import config
import component

class Car(component.Component):

    jitter = 20

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
        x = config.left_margin + self.lane * config.cell_width
        y = self.speed * config.row_height
        x += random.randrange(self.jitter) - self.jitter/2
        y += random.randrange(self.jitter) - self.jitter/2
        surface.blit(self.texture, (x, y))
