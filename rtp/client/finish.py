import pygame
from rtp.common import config
import component


class FinishLine(component.Component):

    def __init__(self):
        self.texture = None
        self.timeleft = config.game_duration

    # Component interface

    def init(self):
        self.texture = pygame.image.load(config.finish_line_png)

    def update(self, info):
        self.timeleft = info["timeleft"]

    def draw(self, surface):
        if self.timeleft > config.finish_line_duration:
            return
        # Start at row 0, then move down until row finish_line_duration
        row = config.finish_line_duration - self.timeleft
        y = config.dashboard_height + config.row_height * row
        surface.blit(self.texture, (0, y))
