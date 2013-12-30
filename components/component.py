class Component(object):
    """ Component intarface """

    def init(self):
        """
        Called when application is initialized.
        """

    def update(self, info):
        """
        Called when gate state changes

        info: dictionary with changes received from game server.
        """


    def draw(self, surface):
        """
        Called when a component should draw itself on surface.

        surface: pygame.Surface object
                 http://www.pygame.org/docs/ref/surface.html
        """
