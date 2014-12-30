import random
import operator
from twisted.internet import reactor, task

from rtp.common import actions, config, error, message, obstacles
import track
import player


class Game(object):
    """
    Implements the server for the car race
    """

    def __init__(self):
        self.server = None
        self.track = track.Track()
        self.looper = task.LoopingCall(self.loop)
        self.players = {}
        self.free_cars = set(range(config.number_of_cars))
        self.free_lanes = set(range(config.max_players))
        self._rate = config.game_rate
        self.started = False
        self._duration = config.game_duration

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
        self.track.reset()
        for player in self.players.values():
            player.reset()
        self.looper.start(1.0 / self._rate)
        self.started = True

    def stop(self):
        if not self.started:
            raise error.GameNotStarted()
        self.looper.stop()
        self.started = False
        self.print_stats()

    def add_player(self, name):
        if name in self.players:
            raise error.PlayerExists(name)
        if not self.free_cars:
            raise error.TooManyPlayers()
        car = random.choice(tuple(self.free_cars))
        self.free_cars.remove(car)
        lane = random.choice(tuple(self.free_lanes))
        self.free_lanes.remove(lane)
        print 'add player:', name, 'lane:', lane, 'car:', car
        self.players[name] = player.Player(name, car, lane)
        reactor.callLater(0, self.update_players)

    def remove_player(self, name):
        if name not in self.players:
            raise error.NoSuchPlayer(name)
        player = self.players.pop(name)
        self.free_cars.add(player.car)
        self.free_lanes.add(player.lane)
        print 'remove player:', name, 'lane:', player.lane, 'car:', player.car
        reactor.callLater(0, self.update_players)

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

    def print_stats(self):
        print
        print 'Stats'
        for i, p in enumerate(sorted(self.players.values())):
            print '%d  %10s  row:%d  life:%d' % (i+1, p.name, p.position.y, p.life)
        print

    def loop(self):
        self._duration -= 1
        if self._duration < 0:
            self.stop()
            return
        self.track.update()
        self.process_actions()
        self.update_players()

    def update_players(self):
        msg = message.Message('update', self.state())
        self.server.broadcast(msg)

    def state(self):
        return {'started': self.started,
                'track': self.track.state(),
                'players': self.players_state(),
                'timeleft': self._duration}

    def players_state(self):
        return dict((name, player.state()) for name, player in
                    self.players.iteritems())

    def process_actions(self):
        # Process first the leading drivers, preferring those with faster
        # response time.
        players = sorted(self.players.itervalues(),
                         key=lambda p: (p.position.y , p.response_time))
        positions = set()

        for player in players:

            # First move playe, keeping inside the track

            if player.action == actions.LEFT:
                if player.position.x > 0:
                    player.position.x -= 1
            elif player.action == actions.RIGHT:
                if player.position.x < config.max_players - 1:
                    player.position.x += 1

            # Now check if player hit any obstacle

            obstacle = self.track.get_obstacle(player.position.x, player.position.y)
            if obstacle == obstacles.CRACK:
                if player.action != actions.JUMP:
                    self.track.clear(player.position.x, player.position.y)
                    player.position.y += 1
            elif obstacle in (obstacles.TRASH,
                              obstacles.BIKE,
                              obstacles.BARRIER):
                self.track.clear(player.position.x, player.position.y)
                player.position.y += 1
            elif obstacle == obstacles.WATER:
                if player.action != actions.BRAKE:
                    self.track.clear(player.position.x, player.position.y)
                    player.position.y += 1
            elif obstacle == obstacles.PENGUIN:
                if player.action == actions.PICKUP:
                    self.track.clear(player.position.x, player.position.y)
                    player.position.y -= 1
                    player.life += 1

            # Here we can end the game when player gets out of
            # the track bounds. For now, just keep the player at the same
            # location.
            player.position.y = min(config.matrix_height - 1, max(0, player.position.y))

            # Finally forget action
            player.action = actions.NONE

            # Fix up collisions

            if (player.position.x, player.position.y) in positions:
                print 'fix up collisions for player', player.name
                if player.position.y < config.matrix_height - 1:
                    player.position.y += 1
                elif player.position.x > 0:
                    player.position.x -= 1
                elif player.position.x < config.matrix_width - 1:
                    player.position.x += 1

            print 'process_actions: name=%s car=%s pos=%d,%d response_time=%0.6f life=%d' % (
                    player.name, player.car, player.position.x, player.position.y,
                    player.response_time, player.life)
            positions.add((player.position.x, player.position.y))
