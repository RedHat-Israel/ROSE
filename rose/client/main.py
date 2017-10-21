import logging
import sys

from twisted.internet import reactor, protocol
from twisted.protocols import basic

from rose.common import config, message
import game

log = logging.getLogger('main')

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
            log.info('Unexpected message:', msg.action, msg.payload)


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


def main():
    if len(sys.argv) < 2:
        log.info('usage: rose-client drive-module')
        sys.exit(2)

    with open(sys.argv[1]) as f:
        d = {}
        exec f in d, d

    reactor.connectTCP(d['server_address'], config.game_port,
                       ClientFactory(d['driver_name'], d['drive']))
    reactor.run()
