__author__ = 'emesika'

import pygame
from rtp.common import config
import component


class Splash(component.Component):
    def init(self):
        self.texture = pygame.image.load(config.splash_png)

    def update(self, players):
        return

    def draw(self, surface):
        # TODO render image in center
        self.draw_label(surface, (config.windows_width / 2, config.windows_height / 2))