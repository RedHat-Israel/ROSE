author = 'gickowic'
import pygame, sys


class RacingGamingClient():

    def init_pygame_resources(self):
        pygame.init()
        self.size = 640, 480
        self.bg_color = 0, 0, 0
        self.components = []

    def update(self):
        for component in self.components:
            if component.__hasattr__('update'):
                component.update()

    def draw(self, screen):
        screen.fill(self.bg_color)
        for component in self.components:
            if component.__hasattr__('draw'):
                component.draw()
        pygame.display.flip()

    def init(self):
        for component in self.components:
            if component.__hasattr__('init'):
                if not component.initialized:
                    component.init()

    def main_game_loop(self):
        screen = pygame.display.set_mode(self.size)
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            self.update()
            self.draw(screen)


def main():
    # TODO: Initialize pygame resources
    game = RacingGamingClient()
    game.init_pygame_resources()

    # TODO: Initialize communications server

    # TODO: construct objects (matrix + car)
     ## create car

     ## create matrix

    # TODO: initialize objects
    game.init()

    # move to main game loop:
    game.main_game_loop()


if __name__ == '__main__':
    main()