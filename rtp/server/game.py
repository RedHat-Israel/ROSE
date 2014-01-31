import random
import operator
from twisted.internet import task

from rtp.common import actions, config, error, message, obstacles
import track
import player


class Game(object):
    """
    Implements the server for the car race
    """

    def __init__(self):
        self.server = None
        self.track = None
        self.looper = task.LoopingCall(self.loop)
        self.players = {}
        self.free_cars = set(range(config.max_players))
        self._rate = config.game_rate
        self.started = False

    @property
    def rate(self):
        return self._rate

    @rate.setter
    def rate(self, value):
        if value != self._rate:
            print 'change game rate to %d frames per second' % value
            self._rate = value
            if self.started:
                self.looper.stop()
                self.looper.start(1.0 / self._rate)

    def start(self):
        if self.started:
            raise error.GameAlreadyStarted()
        self.track = track.Track()
        for player in self.players.values():
            player.reset()
        self.looper.start(1.0 / self._rate)
        self.started = True

    def stop(self):
        if not self.started:
            raise error.GameNotStarted()
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

    def remove_player(self, name):
        if name not in self.players:
            raise error.NoSuchPlayer(name)
        player = self.players.pop(name)
        self.free_cars.add(player.lane)
        print 'remove player:', name, 'car:', player.car

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
        self.players[name].response_time = info.get('response_time', 1.0)

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
        # Process first the leading drivers, preferring those with faster
        # response time.
        players = sorted(self.players.itervalues(),
                         key=operator.attrgetter('speed', 'response_time'))
        positions = set()

        for player in players:

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
                    self.track.clear(player.lane, player.speed)
                    player.speed += 1
            elif obstacle in (obstacles.TRASH,
                              obstacles.BIKE,
                              obstacles.BARRIER):
                self.track.clear(player.lane, player.speed)
                player.speed += 1
            elif obstacle == obstacles.WATER:
                if player.action != actions.BRAKE:
                    self.track.clear(player.lane, player.speed)
                    player.speed += 1
            elif obstacle == obstacles.PENGUIN:
                if player.action == actions.PICKUP:
                    self.track.clear(player.lane, player.speed)
                    player.speed -= 1

            # Here we can end the game when player gets out of
            # the track bounds. For now, just keep the player at the same
            # location.
            player.speed = min(config.matrix_height - 1, max(0, player.speed))

            # Finally forget action
            player.action = actions.NONE

            # Fix up collisions

            if (player.lane, player.speed) in positions:
                print 'fix up collisions for player', player.name
                if player.speed < config.matrix_height - 1:
                    player.speed += 1
                elif player.lane > 0:
                    player.lane -= 1
                elif player.lane < config.matrix_width - 1:
                    player.lane += 1

            print 'process_actions: name=%s car=%s pos=%d,%d response_time=%0.6f' % (
                    player.name, player.car, player.lane, player.speed,
                    player.response_time)
            positions.add((player.lane, player.speed))
