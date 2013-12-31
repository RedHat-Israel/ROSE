from twisted.internet import reactor
from twisted.internet import task
from components import matrix
from components import car
from components import message
from components import component
import config

author = 'gickowic'
import pygame, sys


class Game(component.Component):

    def __init__(self, client):
        self.client = client
        self.components = [
            matrix.Matrix(),
            car.Car(1, 0, 4),
            car.Car(2, 1, 4),
            car.Car(3, 2, 4),
            car.Car(4, 3, 4),
        ]
        pygame.init()
        self.surface = pygame.display.set_mode(config.window_size)
        self.looper = task.LoopingCall(self.tick)

        self.init()
        frame_delay = 1.0 / config.frame_rate
        self.looper.start(frame_delay)

    # Component interface

    def init(self):
        pygame.display.set_caption(config.window_caption)
        for component in self.components:
            component.init()
        self.draw(self.surface)

    def update(self, info):
        for component in self.components:
            component.update(info)
        self.draw(self.surface)

    def draw(self, surface):
        surface.fill(config.background_color)
        for component in self.components:
            component.draw(surface)
        pygame.display.flip()

    # Hanlding pygame events

    def tick(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                reactor.stop()

    # Handling client events

    def client_connected(self):
        print 'client connected'
        msg = message.Message('start', None)
        self.client.send_message(msg)

    def client_disconnected(self, reason):
        print 'client disconnected', reason.getErrorMessage()

    def client_failed(self, reason):
        print 'client failed', reason.getErrorMessage()

    def client_update(self, info):
        print 'client_update', info
        self.update(info)

    def client_welcome(self):
        print 'client_welcome'
