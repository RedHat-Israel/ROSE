from twisted.internet import reactor, protocol
from twisted.protocols import basic
from components import message

import game
import config

class Client(basic.LineReceiver):

    id = None

    def connectionMade(self):
        self.factory.connected(self)

    def connectionLost(self, reason):
        self.factory.disconnected(reason)

    def connectionFailed(self, reason):
        self.factory.failed(reason)

    def lineReceived(self, line):
        msg = message.parse(line)
        if msg.action == 'welcome':
            self.id = msg.payload['id']
            self.factory.welcome()
        elif msg.action == 'update':
            self.factory.update(msg.payload)

class ClientFactory(protocol.ReconnectingClientFactory):

    protocol = Client
    initialDelay = 0.1
    maxDelay = 5

    def __init__(self):
        self.game = game.Game(self)
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

    def update(self, info):
        self.game.client_update(info)

    def welcome(self):
        self.game.client_welcome()

    # Client interface

    def send_message(self, msg):
        self.client.sendLine(str(msg))

reactor.connectTCP(config.host, config.port, ClientFactory())
reactor.run()
