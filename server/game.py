import random
from twisted.internet import task
from components import message

from components import matrix
import components.matrix_config as config
from common import error
import player


class Game(object):
    """
    Implements the server for the car race
    """

    def __init__(self, server):
        self.server = server
        self.matrix = matrix.Matrix()
        self.looper = task.LoopingCall(self.loop)
        self.players = {}
        self.free_lanes = set(range(config.MAX_PLAYERS))
        self.started = False

    def start(self):
        assert not self.started
        self.started = True
        self.looper.start(1, now=False)

    def stop(self):
        if self.started:
            self.looper.stop()
            self.started = False

    def add_player(self, name):
        if name in self.players:
            raise error.PlayerExists(name)
        if not self.free_lanes:
            raise error.TooManyPlayers()
        lane = random.choice(tuple(self.free_lanes))
        self.free_lanes.remove(lane)
        print 'add player:', name, 'lane:', lane
        self.players[name] = player.Player(name, lane)
        # Start the game when the first player joins
        if not self.started:
            self.start()

    def remove_player(self, name):
        if name not in self.players:
            raise error.NoSuchPlayer(name)
        player = self.players.pop(name)
        self.free_lanes.add(player.lane)
        print 'remove player:', name, 'lane:', player.lane
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
        self.matrix.advance()
        self.process_actions()
        msg = message.Message('update', self.encode())
        self.server.broadcast(msg)

    def encode(self):
        players = dict((name, player.encode())
                       for name, player in self.players.iteritems())
        return {'matrix': self.matrix.encode(), 'players': players}

    def process_actions(self):
        for player in self.players.values():

            if player.life == 0:
                continue

            # First move playe, keeping inside the track

            if player.action == config.LEFT:
                if player.lane > 0:
                    player.lane -= 1
            elif player.action == config.RIGHT:
                if player.lane < config.MAX_PLAYERS - 1:
                    player.lane += 1

            # Now check if player hit any obstacle

            obstacle = self.matrix.matrix[player.speed][player.lane]
            if obstacle == config.CRACK:
                if player.action != config.JUMP:
                    player.life -= 1
            elif obstacle in (config.TRASH,
                              config.BIKE,
                              config.BARRIER):
                player.life -= 1
            elif obstacle == config.WATER:
                if player.action != config.BRAKE:
                    player.life -= 1
            elif obstacle == config.PENGIUN:
                player.life += 1

            # Set player speed

            speed = config.HEIGHT / 2 - player.life + config.MAX_LIVES
            player.speed = min(config.HEIGHT - 1, max(0, speed))
