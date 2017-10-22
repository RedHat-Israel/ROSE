import random
import operator
from twisted.internet import reactor, task

from rose.common import actions, config, error, message, obstacles
import track
import player
import score


class Game(object):
    """
    Implements the server for the car race
    """

    def __init__(self):
        self.hub = None
        self.track = track.Track()
        self.looper = task.LoopingCall(self.loop)
        self.players = {}
        self.free_cars = set(range(config.number_of_cars))
        self.free_lanes = set(range(config.max_players))
        self._rate = config.game_rate
        self.started = False
        self.timeleft = config.game_duration

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
            else:
                self.update_clients()

    def start(self):
        if self.started:
            raise error.GameAlreadyStarted()
        self.track.reset()
        for player in self.players.values():
            player.reset()
        self.timeleft = config.game_duration
        self.started = True
        self.looper.start(1.0 / self._rate)

    def stop(self):
        if not self.started:
            raise error.GameNotStarted()
        self.looper.stop()
        self.started = False
        self.update_clients()
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
        reactor.callLater(0, self.update_clients)

    def remove_player(self, name):
        if name not in self.players:
            raise error.NoSuchPlayer(name)
        player = self.players.pop(name)
        self.free_cars.add(player.car)
        self.free_lanes.add(player.lane)
        print 'remove player:', name, 'lane:', player.lane, 'car:', player.car
        reactor.callLater(0, self.update_clients)

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
        for i, p in enumerate(sorted(self.players.values(), reverse=True)):
            print '%d  %10s  row:%d  score:%d' % (
                i+1, p.name, p.y, p.score
            )
        print

    def loop(self):
        self.track.update()
        score.process(self.players, self.track)
        if self.timeleft > 0:
            self.update_clients()
            self.timeleft -= 1
        else:
            self.stop()

    def update_clients(self):
        msg = message.Message('update', self.state())
        self.hub.broadcast(msg)

    def state(self):
        return {'started': self.started,
                'track': self.track.state(),
                'players': [p.state() for p in self.players.values()],
                'timeleft': self.timeleft,
                'rate': self.rate}
