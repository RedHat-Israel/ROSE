__author__ = 'talayan'

import pygame
from rtp.common import config
import component


class Dashboard(component.Component):

    TEXT_COLOR = (153, 153, 153)
    TIMER_FONT_SIZE = 70
    INFO_FONT_SIZE = 50
    INFO_LEFT_MARGIN = 50
    INFO_OFFSET = 530

    def init(self):
        self.texture = pygame.image.load(config.dashboard_png)
        self.players = {}
        self.timeleft = config.game_duration

    def update(self, players, timeleft):
        self.timeleft = timeleft
        self.players = players

    def draw(self, surface):
        self._draw_timer(surface)
        self._draw_players_info(surface)

    def _draw_timer(self, surface):
        font = pygame.font.SysFont(pygame.font.get_default_font(),
                                   self.TIMER_FONT_SIZE)
        text = font.render("%02d" % self.timeleft, 1, self.TEXT_COLOR)
        x = config.windows_width / 2 - text.get_width() / 2
        y = config.dashboard_height / 2 - text.get_height() / 2
        surface.blit(text, (x, y))

    def _draw_players_info(self, surface):
        font = pygame.font.SysFont(pygame.font.get_default_font(),
                                   self.INFO_FONT_SIZE)
        for player in self.players.values():
            info = "%(name)s : %(life)d" % player
            text = font.render(info, 1, self.TEXT_COLOR)
            x = self.INFO_LEFT_MARGIN + player["lane"] * self.INFO_OFFSET
            surface.blit(text, (x, config.dashboard_top_margin))
