from twisted.internet import reactor, protocol
from twisted.protocols import basic
from components import message
from common import error
import game


class Player(basic.LineReceiver):

    def __init__(self):
        self.name = None

    def connectionMade(self):
        self.factory.playerConnected(self)

    def connectionLost(self, reason):
        self.factory.playerDisconnected(self)

    def lineReceived(self, line):
        try:
            msg = message.parse(line)
            self.dispatch(msg)
        except error.Error as e:
            msg = message.Message('error', {'message': str(e)})
            self.sendLine(str(msg))
            self.transport.loseConnection()

    def dispatch(self, msg):
        if self.name is None:
            # New player
            if msg.action != 'join':
                raise error.ActionForbidden(msg.action)
            if 'name' not in msg.payload:
                raise error.InvalidMessage("name required")
            name = msg.payload['name']
            # Will raise if there are too many players or this name is already
            # taken, leaving me in non-registered state.
            self.factory.registerPlayer(name)
            # I was registered successfully
            self.name = name
        else:
            # Registered player
            if msg.action == 'start':
                self.factory.start()
            elif msg.action == 'update':
                self.factory.updatePlayer(self.name, msg.payload)
            else:
                raise error.ActionForbidden(msg.action)

class Server(protocol.ServerFactory):
    protocol = Player

    def __init__(self):
        self.game = game.Game(self)
        self.players = set()

    def playerConnected(self, player):
        self.players.add(player)

    def playerDisconnected(self, player):
        self.players.remove(player)
        if player.name is not None:
            self.game.remove_player(player.name)

    def registerPlayer(self, name):
        self.game.add_player(name)

    def updatePlayer(self, name, info):
        self.game.update_player(name, info)

    def start(self):
        if not self.game.started:
            self.game.start()

    def broadcast(self, msg):
        data = str(msg)
        for player in self.players:
            if player.name is not None:
                player.sendLine(data)


reactor.listenTCP(8888, Server())
reactor.run()

