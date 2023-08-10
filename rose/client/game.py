import logging
import time

import six

from twisted.internet import reactor

from rose.common import message
from . import track
from . import car
from . import world
from . import component

author = 'gickowic'
log = logging.getLogger('game')


class Game(component.Component):

    def __init__(self, client, name, drive_func,seed):
        self.client = client
        self.drive_func = drive_func
        self.name = name
        self.track = track.Track()
        self.players = {}
        self.seed = seed
        self.cars = [car.Car(1),
                     car.Car(2),
                     car.Car(3),
                     car.Car(4)]
        self.world = world.generate_world(self)
    def get_seed(self):
        return self.seed
    # Component interface
    def update(self, info):
        self.track.update(info)
        self.players = {p["name"]: p for p in info['players']}
        for player in six.itervalues(self.players):
            self.cars[player['car']].update(player)
        if info['started']:
            self.drive()

    # Driving

    def drive(self):
        start = time.time()
        try:
            action = self.drive_func(self.world)
        except Exception:
            # Make it easy to detect and handle errors by crashing loudly. In
            # the past we used to print a traceback and continue, and students
            # had trouble detecting and handling errors.
            reactor.stop()
            raise
        response_time = time.time() - start
        msg = message.Message('drive', {"action": action,
                                        "response_time": response_time})
        self.client.send_message(msg)

    # Accessing

    @property
    def car(self):
        return self.cars[self.players[self.name]['car']]

    # Handling client events

    def client_connected(self):
        log.info('client connected: joining as %s', self.name)
        msg = message.Message('join', {"name": self.name})
        self.client.send_message(msg)

    def client_disconnected(self, reason):
        log.info('client disconnected: %s', reason.getErrorMessage())

    def client_failed(self, reason):
        log.info('client failed: %s', reason.getErrorMessage())

    def client_error(self, error):
        log.info('client error: %s', error.get('message'))
        reactor.stop()

    def client_update(self, info):
        # print 'client_update', info
        self.update(info)
