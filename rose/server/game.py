import random
import logging
import os

import six

from twisted.internet import reactor, task

from rose.common import actions, config, error, message, obstacles  # NOQA
from . import track
from . import player
from . import score

log = logging.getLogger('game')


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
            log.info('change game rate to %d frames per second', value)
            self._rate = value
            if self.started:
                self.looper.stop()
                self.looper.start(1.0 / self._rate)
            else:
                self.update_clients()

    def start(self):
        if self.started:
            raise error.GameAlreadyStarted()
        if not self.players:
            raise error.ActionForbidden("start a game with no players.")
        self.track.reset()
        for p in six.itervalues(self.players):
            p.reset()
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
        log.info('add player: %r, lane: %r, car: %r', name, lane, car)
        self.players[name] = player.Player(name, car, lane)
        reactor.callLater(0, self.update_clients)

    def remove_player(self, name):
        if name not in self.players:
            raise error.NoSuchPlayer(name)
        player = self.players.pop(name)
        self.free_cars.add(player.car)
        self.free_lanes.add(player.lane)
        log.info('remove player: %r, lane: %r, car: %r',
                 name, player.lane, player.car)
        if not self.players and self.started:
            log.info('Stopping game. No players connected.')
            self.stop()
        else:
            reactor.callLater(0, self.update_clients)

    def drive_player(self, name, info):
        log.info('drive_player: %r %r', name, info)
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
        lines = ['Stats:']
        top_scorers = sorted(six.itervalues(self.players), reverse=True)
        for i, p in enumerate(top_scorers):
            line = '%d  %10s  row:%d  score:%d' % (i + 1, p.name, p.y, p.score)
            lines.append(line)
        log.info("%s", os.linesep.join(lines))

    def loop(self):
        self.track.update()
        score.process(self.players, self.track)
        top_scorers = sorted(six.itervalues(self.players), reverse=True)
        for p in top_scorers:
            if p.score > 0:
                self.update_clients()
                self.timeleft += 1
            else:
                self.stop()

    def update_clients(self):
        msg = message.Message('update', self.state())
        self.hub.broadcast(msg)

    def state(self):
        return {'started': self.started,
                'track': self.track.state(),
                'players': [p.state() for p in six.itervalues(self.players)],
                'timeleft': self.timeleft,
                'rate': self.rate}
