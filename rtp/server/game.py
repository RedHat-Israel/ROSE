import random
from twisted.internet import task

from rtp.common import actions, config, error, message, obstacles
import track
import player


class Game(object):
    """
    Implements the server for the car race
    """

    def __init__(self, server):
        self.server = server
        self.track = track.Track()
        self.looper = task.LoopingCall(self.loop)
        self.players = {}
        self.free_cars = set(range(config.max_players))
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
        if not self.free_cars:
            raise error.TooManyPlayers()
        car = random.choice(tuple(self.free_cars))
        self.free_cars.remove(car)
        print 'add player:', name, 'car:', car
        self.players[name] = player.Player(name, car)
        # Start the game when the first player joins
        if not self.started:
            self.start()

    def remove_player(self, name):
        if name not in self.players:
            raise error.NoSuchPlayer(name)
        player = self.players.pop(name)
        self.free_cars.add(player.lane)
        print 'remove player:', name, 'car:', player.car
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
        if action not in actions.ALL:
            raise error.InvalidMessage("invalid drive action %s" % action)
        self.players[name].action = action

    def loop(self):
        self.track.update()
        self.process_actions()
        msg = message.Message('update', self.state())
        self.server.broadcast(msg)

    def state(self):
        players = dict((name, player.state())
                       for name, player in self.players.iteritems())
        return {'track': self.track.state(), 'players': players}

    def process_actions(self):
        for player in self.players.values():

            # First move playe, keeping inside the track

            if player.action == actions.LEFT:
                if player.lane > 0:
                    player.lane -= 1
            elif player.action == actions.RIGHT:
                if player.lane < config.max_players - 1:
                    player.lane += 1

            # Now check if player hit any obstacle

            obstacle = self.track.get_obstacle(player.lane, player.speed)
            if obstacle == obstacles.CRACK:
                if player.action != actions.JUMP:
                    player.life -= 1
            elif obstacle in (obstacles.TRASH,
                              obstacles.BIKE,
                              obstacles.BARRIER):
                player.life -= 1
            elif obstacle == obstacles.WATER:
                if player.action != actions.BRAKE:
                    player.life -= 1
            elif obstacle == obstacles.PENGIUN:
                player.life += 1
                if player.action == actions.PICKUP:
                    player.life += 1

            # Remove obstacle after collision
            self.track.set_obstacle(player.lane, player.speed, obstacles.NONE)

            # Set player speed

            speed = config.matrix_height / 2 - player.life + config.max_lives
            player.speed = min(config.matrix_height - 1, max(0, speed))

            # Finally forget action
            player.action = actions.NONE
