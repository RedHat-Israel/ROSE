from twisted.internet import reactor, protocol
from twisted.protocols import basic
from components import message
import game


class Player(basic.LineReceiver):

    def __init__(self):
        self.id = None

    def connectionMade(self):
        self.id = self.factory.addPlayer(self)
        msg = message.Message('welcome', {'id': str(self.id)})
        self.sendLine(str(msg))

    def connectionLost(self, reason):
        self.factory.removePlayer(self)

    def lineReceived(self, line):
        msg  = message.parse(line)
        if msg.action == 'start':
            self.factory.start()
        elif msg.action == 'update':
            self.factory.updatePlayer(msg.payload)


class Server(protocol.ServerFactory):
    protocol = Player

    def __init__(self):
        self.game = game.Game(self)
        self.players = {}

    def addPlayer(self, player):
        id = self.game.add_player()
        self.players[id] = player
        return id

    def removePlayer(self, player):
        self.game.remove_player(player.id)
        del self.players[player.id]

    def updatePlayer(self, id, info):
        self.game.update_player(id, info)

    def start(self):
        if not self.game.started:
            self.game.start()

    def broadcast(self, msg):
        for player in self.players.itervalues():
            player.sendLine(msg)


reactor.listenTCP(8888, Server())
reactor.run()

