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
        self.players[name] = Player(name, lane)
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

    def drive_player(self, name, info):
        print 'drive_player:', name, info
        if name not in self.players:
            raise error.NoSuchPlayer(name)
        if 'action' not in info:
            raise error.InvalidMessage("action required")
        action = info['action']
        if action not in config.ACTIONS:
            raise error.InvalidMessage("invalid drive action %s" % action)
        self.players[name].action = action

    def loop(self):
        print 'loop'
        # Send updates to the clients
        # XXX process game logic here (self.do)
        self.matrix.next_row()
        self.process_actions()
        msg = message.Message('update', self.encode())
        self.server.broadcast(msg)

    def encode(self):
        players = dict((name, player.encode())
                       for name, player in self.players.iteritems())
        return {'matrix': self.matrix.encode(), 'players': players}

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
        for player in self.players.values():
            obstacle = self.matrix.matrix[player.speed][player.lane]
            acceptable, default = SCORE[obstacle]
            score = acceptable.get(player.action, default)
            player.life += score

