import random
import pygame
import os
from rose.common import config
import component

class Car(component.Component):

    def __init__(self, id, x, y):
        self.id = id
        self.x = None
        self.y = None
        self.texture = None
        self.name = None

    def init(self):
        path = os.path.join(config.cars_dir, 'car%d.png' % self.id)
        self.texture = pygame.image.load(path)

    def update(self, info):
        self.x = info['x']
        self.y = info['y']
        self.name = info['name']

    def draw(self, surface):
        x = config.left_margin + self.x * config.cell_width
        y = config.dashboard_height + self.y * config.row_height
        x += random.randrange(config.car_jitter) - config.car_jitter/2
        y += random.randrange(config.car_jitter) - config.car_jitter/2
        surface.blit(self.texture, (x, y))
        self.draw_label(surface, (x, y))

    def draw_label(self, surface, (x, y)):
        font = pygame.font.SysFont(pygame.font.get_default_font(), 20)
        text = font.render(self.name, 1, (0,0,0))
        text_x = x + config.row_height / 2 - text.get_width() / 2
        text_y = y + config.row_height + 5
        surface.blit(text, (text_x, text_y))
