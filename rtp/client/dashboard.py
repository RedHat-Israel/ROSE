__author__ = 'talayan'

import pygame
from rtp.common import config
import component


class Dashboard(component.Component):

    def init(self):
        self.texture = pygame.image.load(config.dashboard_png)
        self.players = {}
        self.timer = str(config.game_duration)

    def update(self, players, timeleft):
        self.timer = str(timeleft)
        self.players = players

    def draw(self, surface):
        timer_font = pygame.font.SysFont(pygame.font.get_default_font(), 70)
        timer = timer_font.render(self.timer, 1, (153, 153, 153))
        if int(self.timer) >= 10:
            timer_x_pos = (config.windows_width / 2) - 27
        else:
            timer_x_pos = (config.windows_width / 2) - 15
        surface.blit(timer, (timer_x_pos, 48))
        self.draw_name_and_score(surface, (50, config.player_name_and_score_pos))

    def draw_name_and_score(self, surface, (x, y)):
        font = pygame.font.SysFont(pygame.font.get_default_font(), 50)
        for player in self.players.values():
            name_and_score = "%(name)s : %(life)d" % player
            text = font.render(str(name_and_score), 1, (153, 153, 153))
            surface.blit(text, (x, y))
            x += 550
