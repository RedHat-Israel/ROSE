import random
import socket
import logging
import argparse

from twisted.internet import reactor
from twisted.web import server, static

from autobahn.twisted.resource import WebSocketResource

from rose.common import config
from . import game, net

log = logging.getLogger('main')


def main():
    logging.basicConfig(level=logging.INFO, format=config.logger_format)
    parser = argparse.ArgumentParser(description="ROSE Server")
    parser.add_argument("--track_definition", "-t", dest="track_definition",
                        default="random", choices=["random", "same"],
                        help="Definition of driver tracks: random or same."
                             "If not specified, random will be used.")
    parser.add_argument("--seed", "-s", dest="seed",
                        default="", type=str,
                        help="Definition of driver tracks: random or same."
                             "If not specified, random will be used.")

    args = parser.parse_args()
    """
    If the argument is 'same', the track will generate the obstacles in the
    same place for both drivers, otherwise, the obstacles will be genrated in
    random locations for each driver.
    """
    if args.track_definition == "same":
        config.is_track_random = False
    else:
        config.is_track_random = True

    """
    If the argument is '', the seed will be generated in random, otherwise 
    the seed will be the seed submitted by the user.
    """
    if args.seed == "":
        random.seed(str(random.randint(1, 100000000000000000)))
        config.track_seed = args.seed
    else:
        config.track_seed = args.seed

    log.info(f"The seed is {config.track_seed}")
    random.seed(config.track_seed)

    log.info('starting server')
    g = game.Game()
    h = net.Hub(g)
    reactor.listenTCP(config.game_port, net.PlayerFactory(h))
    root = static.File(config.web_root)
    wsuri = u"ws://%s:%s" % (socket.gethostname(), config.web_port)
    watcher = net.WatcherFactory(wsuri, h)
    root.putChild(b"ws", WebSocketResource(watcher))
    root.putChild(b'res', static.File(config.res_root))
    root.putChild(b'admin', net.WebAdmin(g))
    root.putChild(b'rpc2', net.CliAdmin(g))
    site = server.Site(root)
    reactor.listenTCP(config.web_port, site)
    reactor.run()
