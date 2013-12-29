from twisted.internet import reactor, protocol
from twisted.protocols import basic
from components import message

import racing_game
import config

class Client(basic.LineReceiver):

    id = None

    def lineReceived(self, line):
        msg = message.parse(line)
        if msg.action == 'welcome':
            self.id = msg.payload['id']
            self.factory.welcome()
        elif msg.action == 'update':
            self.factory.update(msg.payload)

class ClientFactory(protocol.ClientFactory):

    protocol = Client

    def __init__(self):
        self.game = racing_game.RacingGamingClient(self)
        self.client = None

    def clientConnectionMade(self, connector):
        self.client = connector
        self.game.client_connected()

    def clientConnectionLost(self, connector, reason):
        self.client = None
        self.game.client_disconnected(reason)
        self.reconnect()

    def clientConnectionFailed(self, connector, reason):
        self.client = None
        self.game.client_failed(reason)
        self.reconnect()

    def reconnect(self):
        reactor.callLater(0.1, reactor.connectTCP, config.host, config.port, self)

    # Client events

    def update(self, info):
        self.game.client_update(info)

    def welcome(self):
        self.game.client_welcome()

    # Client interface

    def send_message(self, msg):
        self.client.sendLine(str(msg))

reactor.connectTCP(config.host, config.port, ClientFactory())
reactor.run()
