from collections import namedtuple
from twisted.internet import reactor
from twisted.internet import task
import pygame
from components import track, car, message, component, world
from common import config

author = 'gickowic'


class Game(component.Component):

    def __init__(self, client, name, drive_func):
        self.client = client
        self.drive_func = drive_func
        self.name = name
        self.track = track.Track()
        self.players = {}
        self.cars = [car.Car(1, 0, 4),
                     car.Car(2, 1, 4),
                     car.Car(3, 2, 4),
                     car.Car(4, 3, 4)]
        pygame.init()
        self.surface = pygame.display.set_mode(config.window_size)
        self.looper = task.LoopingCall(self.tick)

        self.init()
        frame_delay = 1.0 / config.frame_rate
        self.looper.start(frame_delay)

    # Component interface

    def init(self):
        pygame.display.set_caption(config.window_caption + ' - ' + self.name)
        self.track.init()
        for car in self.cars:
            car.init()
        self.draw(self.surface)

    def update(self, info):
        self.track.update(info)
        self.players = info['players']
        for player in self.players.itervalues():
            self.cars[player['car']].update(player)
        self.draw(self.surface)

        client_car = self.cars[self.players[self.name]['car']]
        car_location = namedtuple('CarLocation', ['x', 'y'])
        car_location.x = client_car.lane
        car_location.y = client_car.speed
        action = self.drive_func(car_location, world.world(self.track))
        msg = message.Message('drive', {"action": action})
        self.client.send_message(msg)

    def draw(self, surface):
        surface.fill(config.background_color)
        self.track.draw(surface)
        for player in self.players.itervalues():
            self.cars[player['car']].draw(surface)
        pygame.display.flip()

    # Hanlding pygame events

    def tick(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                reactor.stop()

    # Handling client events

    def client_connected(self):
        print 'client connected: joining as', self.name
        msg = message.Message('join', {"name": self.name})
        self.client.send_message(msg)

    def client_disconnected(self, reason):
        print 'client disconnected:', reason.getErrorMessage()

    def client_failed(self, reason):
        print 'client failed:', reason.getErrorMessage()

    def client_error(self, error):
        print 'client error:', error.get('message')

    def client_update(self, info):
        print 'client_update', info
        self.update(info)
