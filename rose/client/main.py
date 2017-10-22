import imp
import os.path
import sys

from twisted.internet import reactor, protocol
from twisted.protocols import basic

from rose.common import config, message
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

def load_driver_module(file_path):
    """
    Title Try to load the driver module from file

    Arguments:
      file_path (str): The path to the driver module

    Returns:
        Driver module (module)

    Raises:
        ImportError if the module cannot be loaded
    """
    module_dir, module_name = os.path.split(os.path.splitext(file_path)[0])
    fp, pathname, description = imp.find_module(module_name, [module_dir])
    try:
        return imp.load_module(module_name, fp, pathname, description)
    finally:
        # Since we may exit via an exception, close fp explicitly.
        if fp:
            fp.close()


def main():
    if len(sys.argv) < 2:
        print 'usage: rose-client drive-module'
        sys.exit(2)
    try:
        driver_mod = load_driver_module(sys.argv[1])
    except ImportError:
        print "Couldn't load driver file"
        sys.exit(2)

    reactor.connectTCP(driver_mod.server_address, config.game_port,
                       ClientFactory(driver_mod.driver_name, driver_mod.drive))
    reactor.run()
