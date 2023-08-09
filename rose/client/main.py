import random
import argparse
import imp
import logging
import os.path
import sys

from twisted.internet import reactor, protocol
from twisted.protocols import basic

from rose.common import config, message
from . import game

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
            log.info('Unexpected message: %s %s', msg.action, msg.payload)


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
        self.client.sendLine(str(msg).encode('utf-8'))


def load_driver_module(file_path):
    """
    Load the driver module from file

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
    logging.basicConfig(level=logging.INFO, format=config.logger_format)
    parser = argparse.ArgumentParser(description="ROSE Client")
    parser.add_argument("--server-address", "-s", dest="server_address",
                        default="localhost",
                        help="The server address to connect to."
                             " For example: '10.20.30.44' or 'my-server.com'."
                             " If not specified, localhost will be used.")

    parser.add_argument("driver_file",
                        help="The path to the driver python module")

    parser.add_argument("--seed", "-se", dest="seed",
                        default="", type=str,
                        help="Definition of driver tracks: random or same."
                             "If not specified, random will be used.")
    args = parser.parse_args()

    with open("seed.txt", "w") as f:
        f.write(args.seed)

    try:
        driver_mod = load_driver_module(args.driver_file)
    except ImportError as e:
        log.error("error loading driver module %r: %s", args.driver_file, e)
        sys.exit(2)

    reactor.connectTCP(args.server_address, config.game_port,
                       ClientFactory(driver_mod.driver_name, driver_mod.drive))

    url = "http://%s:%d" % (args.server_address, config.web_port)
    log.info("Please open %s to watch the game." % url)

    reactor.run()
