class Component(object):
    """ Component intarface """

    def update(self, info):
        """
        Called when gate state changes

        info: dictionary with changes received from game server.
        """
