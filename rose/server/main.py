import json
from twisted.internet import reactor, protocol
from twisted.protocols import basic
from twisted.web import http, resource, server, static, xmlrpc
from rose.common import config, error, message
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
            elif msg.action == 'drive':
                self.factory.drivePlayer(self.name, msg.payload)
            else:
                raise error.ActionForbidden(msg.action)

class Server(protocol.ServerFactory):
    protocol = Player

    def __init__(self, game):
        game.server = self
        self.game = game
        self.players = set()

    def playerConnected(self, player):
        self.players.add(player)

    def playerDisconnected(self, player):
        self.players.remove(player)
        if player.name is not None:
            self.game.remove_player(player.name)

    def registerPlayer(self, name):
        self.game.add_player(name)

    def drivePlayer(self, name, info):
        self.game.drive_player(name, info)

    def start(self):
        if not self.game.started:
            self.game.start()

    def broadcast(self, msg):
        data = str(msg)
        for player in self.players:
            if player.name is not None:
                player.sendLine(data)

class XMLRPC(xmlrpc.XMLRPC):

    def __init__(self, game):
        self.game = game
        xmlrpc.XMLRPC.__init__(self, allowNone=True)

    def xmlrpc_start(self):
        try:
            self.game.start()
        except error.GameAlreadyStarted as e:
            raise xmlrpc.Fault(1, str(e))

    def xmlrpc_stop(self):
        try:
            self.game.stop()
        except error.GameNotStarted as e:
            raise xmlrpc.Fault(1, str(e))

    def xmlrpc_set_rate(self, rate):
        self.game.rate = rate

class WebAdmin(resource.Resource):

    def __init__(self, game):
        self.game = game
        resource.Resource.__init__(self)

    def render_GET(self, request):
        request.setHeader(b"content-type", b"application/json")
        return json.dumps(self.game.state())

    def render_POST(self, request):
        if "running" in request.args:
            value = request.args["running"][0]
            if value == "1":
                self.game.start()
            elif value == "0":
                if self.game.started:
                    self.game.stop()
            else:
                request.setResponseCode(http.BAD_REQUEST)
                return b"Invalid running value %r, expected (1, 0)" % value
        return ""

def main():
    g = game.Game()
    reactor.listenTCP(config.game_port, Server(g))
    root = static.File(config.web_root)
    root.putChild('admin', WebAdmin(g))
    root.putChild('rpc2', XMLRPC(g))
    site = server.Site(root)
    reactor.listenTCP(config.web_port, site)
    reactor.run()
