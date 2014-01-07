import sys

from twisted.internet import reactor, protocol
from twisted.protocols import basic

from components import message
from common import config
import game


class Client(basic.LineReceiver):

    def connectionMade(self):
        self.factory.connected(self)

    def connectionLost(self, reason):
        self.factory.disconnected(reason)

    def connectionFailed(self, reason):
        self.factory.failed(reason)

    def lineReceived(self, line):
        msg = message.parse(line)
        if msg.action == 'update':
            self.factory.update(msg.payload)
        elif msg.action == 'error':
            self.factory.error(msg.payload)
        else:
            print 'Unexpected message:', msg.action, msg.payload


class ClientFactory(protocol.ReconnectingClientFactory):

    protocol = Client
    initialDelay = 2
    maxDelay = 2

    def __init__(self, name, drive_func):
        self.game = game.Game(self, name, drive_func)
        self.client = None

    # Client events

    def connected(self, client):
        self.resetDelay()
        self.client = client
        self.game.client_connected()

    def disconnected(self, reason):
        self.client = None
        self.game.client_disconnected(reason)

    def failed(self, reason):
        self.client = None
        self.game.client_failed(reason)

    def error(self, error):
        self.game.client_error(error)

    def update(self, info):
        self.game.client_update(info)

    # Client interface

    def send_message(self, msg):
        self.client.sendLine(str(msg))

if len(sys.argv) < 3:
    print 'usage: start_client player-name player-drive_module'
    sys.exit(2)

with open(sys.argv[2]) as f:
    d = {}
    exec f in d, d

reactor.connectTCP(config.host, config.port, ClientFactory(sys.argv[1],
                                                           d['drive']))
reactor.run()
