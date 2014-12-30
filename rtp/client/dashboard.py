__author__ = 'talayan'

import pygame
from rtp.common import config
import component

class Dashboard(component.Component):

    def init(self):
        self.texture = pygame.image.load(config.dashboard_png)
        self.players = {}

    def update(self, players):
        '''
        :param info:
        :return:
        '''
        for player in players.itervalues():
            self.players[player['name']] = player['life']


    def draw(self, surface):
        player_font = pygame.font.SysFont(pygame.font.get_default_font(), 50)
        score_font = pygame.font.SysFont(pygame.font.get_default_font(), 40)
        position_x = 50
        position_score_x = 85
        for name, score in self.players.iteritems():
            player_name = player_font.render(name, 1, (153, 153, 153))
            player_score = score_font.render(str(score), 1, (153, 153, 153))
            surface.blit(player_name, (position_x, config.player_name_pos ))
            surface.blit(player_score, (position_score_x, config.player_score_pos ))
            position_x += 550
            position_score_x = 610
