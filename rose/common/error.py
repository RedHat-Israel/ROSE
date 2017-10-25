class Error(Exception):
    """ Base class for server errors """
    def __str__(self):
        return self.message % self.args


class PlayerExists(Error):
    message = "Player exists: %s"

    def __init__(self, name):
        self.args = (name,)


class TooManyPlayers(Error):
    message = "Too many players"


class NoSuchPlayer(Error):
    def __init__(self, name):
        self.args = (name,)
    message = "No such player: %s"


class ActionForbidden(Error):
    def __init__(self, action):
        self.args = (action,)
    message = "You are not allowed to %s"


class InvalidMessage(Error):
    def __init__(self, reason):
        self.args = (reason,)
    message = "Invalid message: %s"


class GameAlreadyStarted(Error):
    message = "Game already started"


class GameNotStarted(Error):
    message = "Game not started yet"
