__author__ = 'talayan'

import pygame
from rtp.common import config
import component


class Dashboard(component.Component):

    TIMER_FONT_COLOR = (153, 153, 153)
    NAMES_FONT_COLOR = (153, 153, 153)
    TIMER_FONT_SIZE = 70
    NAMES_FONT_SIZE = 50
    NAMES_START_POS = 50
    NAMES_OFFSET_BETWEEN_SCORES = 530
    TIMER_X_OFFSET = 27
    TIMER_Y_OFFSET = 48

    def init(self):
        self.texture = pygame.image.load(config.dashboard_png)
        self.players = {}
        self.timeleft = config.game_duration

    def update(self, players, timeleft):
        self.timeleft = timeleft
        self.players = players

    def draw(self, surface):
        self._draw_timer(surface)
        self._draw_name_and_score(surface)

    def _draw_timer(self, surface):
        timer_font = pygame.font.SysFont(pygame.font.get_default_font(),
                                         Dashboard.TIMER_FONT_SIZE)
        timer = timer_font.render("%02d" % self.timeleft, 1,
                                  Dashboard.TIMER_FONT_COLOR)
        timer_x_pos = (config.windows_width / 2) - Dashboard.TIMER_X_OFFSET
        surface.blit(timer, (timer_x_pos, Dashboard.TIMER_Y_OFFSET))

    def _draw_name_and_score(self, surface):
        font = pygame.font.SysFont(pygame.font.get_default_font(),
                                   Dashboard.NAMES_FONT_SIZE)
        for player in self.players.values():
            name_and_score = "%(name)s : %(life)d" % player
            text = font.render(str(name_and_score), 1,
                               Dashboard.NAMES_FONT_COLOR)
            x = (Dashboard.NAMES_START_POS +
                 player["lane"] * Dashboard.NAMES_OFFSET_BETWEEN_SCORES)
            surface.blit(text, (x, config.dashboard_top_margin))
