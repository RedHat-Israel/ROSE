class Error(Exception):
    """ Base class for server errors """
    def __str__(self):
        return self.message.format(self.args)


class PlayerExists(Error):
    message = "Player exists: {}"

    def __init__(self, name):
        self.args = (name,)


class TooManyPlayers(Error):
    message = "Too many players"


class NoSuchPlayer(Error):
    def __init__(self, name):
        self.args = (name,)
    message = "No such player: {}"


class ActionForbidden(Error):
    def __init__(self, action):
        self.args = (action,)
    message = "You are not allowed to {}"


class InvalidMessage(Error):
    def __init__(self, reason):
        self.args = (reason,)
    message = "Invalid message: {}"


class GameAlreadyStarted(Error):
    message = "Game already started"


class GameNotStarted(Error):
    message = "Game not started yet"
