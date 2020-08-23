import argparse
import socket
import logging

from twisted.internet import reactor
from twisted.web import server, static

from autobahn.twisted.resource import WebSocketResource

from rose.common import config
from . import game, net

log = logging.getLogger('main')


def main():
    logging.basicConfig(level=logging.INFO, format=config.logger_format)
    parser = argparse.ArgumentParser(description="ROSE Server")
    parser.add_argument("--server-port", "-p", dest="server_port",
                        default=config.game_port,
                        type=int,
                        help="The server port to connect to."
                             " For example: '7173'"
                             " If not specified, 8888 will be used.")
    parser.add_argument("--web-port", "-wp", dest="web_port",
                        default=config.web_port,
                        type=int,
                        help="The server port to connect to web UI in browser."
                             " For example: '6261'"
                             " If not specified, 8880 will be used.")

    args = parser.parse_args()

    log.info('Starting server on port:%s' % args.server_port)
    g = game.Game()
    h = net.Hub(g)
    reactor.listenTCP(args.server_port, net.PlayerFactory(h))
    root = static.File(config.web_root)
    wsuri = u"ws://%s:%s" % (socket.gethostname(), args.web_port)
    watcher = net.WatcherFactory(wsuri, h)
    root.putChild(b"ws", WebSocketResource(watcher))
    root.putChild(b'res', static.File(config.res_root))
    root.putChild(b'admin', net.WebAdmin(g))
    root.putChild(b'rpc2', net.CliAdmin(g))
    site = server.Site(root)
    reactor.listenTCP(args.web_port, site)
    reactor.run()
