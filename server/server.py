import json
import time
from twisted.internet import reactor, protocol, task
from twisted.protocols import basic

class Player(basic.LineReceiver):

    def connectionMade(self):
        self.factory.addPlayer(self)

    def connectionLost(self, reason):
        self.factory.removePlayer(self)

    def lineReceived(self, msg):
        if msg == 'start':
            self.factory.start()

class Game(protocol.ServerFactory):
    protocol = Player

    def __init__(self):
        self.players = set()
        self.looper = task.LoopingCall(self.loop)
        self.board = None

    def addPlayer(self, player):
        self.players.add(player)

    def removePlayer(self, player):
        self.players.remove(player)

    def start(self):
        self.board = [
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0],
        ]
        msg = json.dumps(self.board)
        self.broadcast(msg)
        self.looper.start(1, now=False)

    def loop(self):
        next_row = [1, 2, 3, 4]
        self.board.pop()
        self.board.insert(0, next_row)
        msg = json.dumps(next_row) 
        self.broadcast(msg)

    def broadcast(self, msg):
        for player in self.players:
            player.sendLine(msg)


reactor.listenTCP(8888, Game())
reactor.run()

