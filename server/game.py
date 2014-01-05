from twisted.internet import task
from components import message

from components import matrix
import components.matrix_config as config
from common import error
from components.matrix_config import SCORE


from player import Player
import random


MAX_PLAYERS = 4
MAX_LANES = 4


class Game(object):
    """
    Implements the server for the car race
    """

    def __init__(self, server):
        self.server = server
        self.matrix = matrix.Matrix()
        self.lives = [config.NUM_OF_LIVES,
                      config.NUM_OF_LIVES,
                      config.NUM_OF_LIVES,
                      config.NUM_OF_LIVES]
        self.looper = task.LoopingCall(self.loop)
        self.players = {}
        self.started = False

    def start(self):
        assert not self.started
        self.started = True
        self.looper.start(1, now=False)

    def stop(self):
        self.looper.stop()
        self.started = False

    def check_lane_availability(self, lane):
        for p in self.players:
            if p.lane == lane:
                return False

        return True

    def find_available_lane(self):
        picked_lane = random.randrange(MAX_LANES)
        while self.check_lane_availability(picked_lane):
            picked_lane = random.randrange(MAX_LANES)
        return picked_lane

    def add_player(self, name):
        if name in self.players:
            raise error.PlayerExists(name)
        if len(self.players) == MAX_PLAYERS:  # XXX add server/config.py
            raise error.TooManyPlayers()
        print 'add player:', name
        lane = self.find_available_lane()
        self.players[name] = Player(lane)
        # Start the game when the first player joins
        if not self.started:
            self.start()

    def remove_player(self, name):
        if name not in self.players:
            raise error.NoSuchPlayer(name)
        print 'remove player:', name
        del self.players[name]
        # Stop the game when the first player leave
        if not self.players:
            self.stop()

    def update_player(self, name, info):
        print 'update_player:', name, info

    def loop(self):
        print 'loop'
        # Send updates to the clients
        # XXX process game logic here (self.do)
        self.process_actions()
        self.matrix.next_row()
        msg = message.Message('update', {'matrix': self.matrix.matrix,
                                         'players': self.players})
        self.server.broadcast(msg)

    def get_next(self):
        """
        Returns the next row
        """
        return self.matrix.next_row()

    def process_actions(self):
        """
        Gets action for each car
        Returns the new position of each car
        Available actions are:
        - Move forward
        - Move right
        - Move left
        - Jump
        - Pick (star)
        """
        for player in self.players:
            obstacle = self.matrix.get_obstacle(player.lane, player.speed)
            score = SCORE[obstacle][0].get(player.action, SCORE[obstacle][1])
            player.life += score
