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
    TIMER_X_TWO_DIGEST_OFFSET = 27
    TIMER_X_ONE_DIGEST_OFFSET = 15
    TIMER_Y_OFFSET = 48

    def init(self):
        self.texture = pygame.image.load(config.dashboard_png)
        self.players = {}
        self.timer = str(config.game_duration)

    def update(self, players, timeleft):
        self.timer = str(timeleft)
        self.players = players

    def draw(self, surface):
        timer_font = pygame.font.SysFont(pygame.font.get_default_font(),
                                         Dashboard.TIMER_FONT_SIZE)
        timer = timer_font.render(self.timer, 1, Dashboard.TIMER_FONT_COLOR)
        if int(self.timer) >= 10:
            timer_x_pos = (config.windows_width / 2) - \
                    Dashboard.TIMER_X_TWO_DIGEST_OFFSET
        else:
            timer_x_pos = (config.windows_width / 2) - \
                    Dashboard.TIMER_X_ONE_DIGEST_OFFSET

        surface.blit(timer, (timer_x_pos, Dashboard.TIMER_Y_OFFSET))
        self.draw_name_and_score(surface, (Dashboard.NAMES_START_POS,
                                 config.player_name_and_score_pos))

    def draw_name_and_score(self, surface, (x, y)):
        font = pygame.font.SysFont(pygame.font.get_default_font(),
                                   Dashboard.NAMES_FONT_SIZE)
        for player in self.players.values():
            name_and_score = "%(name)s : %(life)d" % player
            text = font.render(str(name_and_score), 1,
                               Dashboard.NAMES_FONT_COLOR)
            surface.blit(text, (x, y))
            x += Dashboard.NAMES_OFFSET_BETWEEN_SCORES
