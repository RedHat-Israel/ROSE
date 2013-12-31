from twisted.internet import reactor
from twisted.internet import task
from components import matrix
from components import message
import config

author = 'gickowic'
import pygame, sys


class Game(object):

    def __init__(self, client):
        self.client = client
        self.init_pygame_resources()
        # TODO: construct objects (matrix + car)
        ## create car

        self.add_component(matrix.Matrix())

        self.init()
        self.looper = task.LoopingCall(self.tick)
        frame_delay = 1.0 / config.frame_rate
        self.looper.start(frame_delay)
        self.screen = pygame.display.set_mode(self.size)

    def init_pygame_resources(self):
        pygame.init()
        self.size = 650, 585
        self.bg_color = 0, 0, 0
        self.components = []

    def add_component(self, component):
        self.components.append(component)

    def update(self, info):
        for component in self.components:
            if hasattr(component, 'update'):
                component.update(info)
        self.draw()

    def draw(self):
        self.screen.fill(self.bg_color)
        for component in self.components:
            if hasattr(component, 'draw'):
                component.draw(self.screen)
        pygame.display.flip()

    def init(self):
        for component in self.components:
            if hasattr(component, 'init'):
                    component.init()

    def tick(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                reactor.stop()

    # Client events

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
