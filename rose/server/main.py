import socket

from twisted.internet import reactor
from twisted.web import server, static

from autobahn.twisted.resource import WebSocketResource

from rose.common import config
from .game import Game
from .net import Hub, PlayerFactory, WebAdmin, CliAdmin


def main():
    g = Game()
    h = Hub(g)
    reactor.listenTCP(config.game_port, PlayerFactory(h))
    root = static.File(config.web_root)
    wsuri = u"ws://%s:%s" % (socket.gethostname(), config.web_port)
    watcher = WatcherFactory(wsuri, h)
    root.putChild("ws", WebSocketResource(watcher))
    root.putChild('res', static.File(config.res_root))
    root.putChild('admin', WebAdmin(g))
    root.putChild('rpc2', CliAdmin(g))
    site = server.Site(root)
    reactor.listenTCP(config.web_port, site)
    reactor.run()
