import socket
import logging

from twisted.internet import reactor
from twisted.web import server, static

from autobahn.twisted.resource import WebSocketResource

from rose.common import config
from . import game, net

log = logging.getLogger('main')

def main():
    logging.basicConfig(level=logging.INFO)
    log.info('starting server')
    g = game.Game()
    h = net.Hub(g)
    reactor.listenTCP(config.game_port, net.PlayerFactory(h))
    root = static.File(config.web_root)
    wsuri = u"ws://%s:%s" % (socket.gethostname(), config.web_port)
    watcher = net.WatcherFactory(wsuri, h)
    root.putChild("ws", WebSocketResource(watcher))
    root.putChild('res', static.File(config.res_root))
    root.putChild('admin', net.WebAdmin(g))
    root.putChild('rpc2', net.CliAdmin(g))
    site = server.Site(root)
    reactor.listenTCP(config.web_port, site)
    reactor.run()
