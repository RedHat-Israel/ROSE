import time
from twisted.internet import reactor
from twisted.internet import task
import pygame

from rose.common import config, message
from . import track, car, component, dashboard, finish, world

author = 'gickowic'


class Game(component.Component):

    def __init__(self, client, name, drive_func):
        self.client = client
        self.drive_func = drive_func
        self.name = name
        self.track = track.Track()
        self.dashboard = dashboard.Dashboard()
        self.finish_line = finish.FinishLine()
        self.players = {}
        self.cars = [car.Car(1, 0, 4),
                     car.Car(2, 1, 4),
                     car.Car(3, 2, 4),
                     car.Car(4, 3, 4)]
        self.world = world.generate_world(self)
        pygame.init()
        self.surface = pygame.display.set_mode(config.window_size)
        self.looper = task.LoopingCall(self.tick)

        self.init()
        frame_delay = 1.0 / config.frame_rate
        self.looper.start(frame_delay)

    # Component interface

    def init(self):
        if config.play_sound:
            pygame.mixer.music.load(config.soundfile)
            pygame.mixer.music.play(-1)
        pygame.display.set_caption(config.window_caption + ' - ' + self.name)

        self.track.init()
        self.dashboard.init()
        for car in self.cars:
            car.init()
        self.finish_line.init()
        self.draw(self.surface)

    def update(self, info):
        self.track.update(info)
        self.players = {p["name"]: p for p in info['players']}
        self.dashboard.update(self.players, info["timeleft"])
        for player in self.players.itervalues():
            self.cars[player['car']].update(player)
        self.finish_line.update(info)
        self.draw(self.surface)
        if info['started']:
            self.drive()

    def draw(self, surface):
        surface.fill(config.background_color)
        self.track.draw(surface)
        self.dashboard.draw(surface)
        for player in self.players.itervalues():
            self.cars[player['car']].draw(surface)
        self.finish_line.draw(surface)
        pygame.display.flip()

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

    # Hanlding pygame events

    def tick(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                reactor.stop()

    # Accessing

    @property
    def car(self):
        return self.cars[self.players[self.name]['car']]

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
        reactor.stop()

    def client_update(self, info):
        # print 'client_update', info
        self.update(info)
