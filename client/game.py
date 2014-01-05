from twisted.internet import reactor
from twisted.internet import task
from components import matrix, car, message, component
import config

author = 'gickowic'
import pygame


class Game(component.Component):

    def __init__(self, client, name, drive_func):
        self.client = client
        self.drive_func = drive_func
        self.name = name
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
        pygame.display.set_caption(config.window_caption + ' - ' + self.name)
        for component in self.components:
            component.init()
        self.draw(self.surface)

    def update(self, info):
        for component in self.components:
            component.update(info)
        self.draw(self.surface)

        action = self.drive_func()

        msg = message.Message('drive', {"action": action})
        self.client.send_message(msg)

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
