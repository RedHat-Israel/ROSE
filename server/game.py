from twisted.internet import reactor, task
from components import message

from components import matrix
import components.matrix_config as config
from common import error

class Game(object):
    """
    Implements the server for the car race
    """

    def __init__(self, server):
        self.server = server
        self.matrix = matrix.Matrix()
        self.lives = [config.NUM_OF_LIVES,
                      config.NUM_OF_LIVES,
                      config.NUM_OF_LIVES,
                      config.NUM_OF_LIVES]
        self.looper = task.LoopingCall(self.loop)
        self.players = {}
        self.started = False

    def start(self):
        assert not self.started
        self.started = True
        self.looper.start(1, now=False)

    def stop(self):
        self.looper.stop()
        self.started = False

    def add_player(self, name):
        if name in self.players:
            raise error.PlayerExists(name)
        if len(self.players) == 4: # XXX add server/config.py
            raise error.TooManyPlayers()
        print 'add player:', name
        self.players[name] = None  # XXX Needs a player class here
        # Start the game when the first player joins
        if not self.started:
            self.start()

    def remove_player(self, name):
        if name not in self.players:
            raise error.NoSuchPlayer(name)
        print 'remove player:', name
        del self.players[name]
        # Stop the game when the first player leave
        if not self.players:
            self.stop()

    def update_player(self, name, info):
        print 'update_player:', name, info

    def loop(self):
        print 'loop'
        # Send updates to the clients
        # XXX process game logic here (self.do)
        self.matrix.next_row()
        msg = message.Message('update', {'matrix': self.matrix.matrix,
                                         'players': self.players})
        self.server.broadcast(msg)

    def get_next(self):
        """
        Returns the next row
        """
        return self.matrix.next_row()

    def do(self, car1_action, car2_action, car3_action, car4_action):
        """
        Gets action for each car
        Returns the new position of each car
        Available actions are:
        - Move forward
        - Move right
        - Move left
        - Jump
        - Pick (star)
        """
        pass

    def _pick(self, car_num):
        """
        Increase life for a car if there is a star there
        """
        x, y = get_location(car_num)
        if get_obstacle(x, y) == ENUMS.STAR:
            self.lives[car_num-1] = self.lives[car_num-1] + 1

    def _get_obstacle(self, x, y):
        """
        Return the obstacle in location x, y
        """
        pass
