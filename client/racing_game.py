from components import matrix

import pygame
import sys


class RacingGamingClient():

    def init_pygame_resources(self):
        pygame.init()
        self.size = 640, 480
        self.bg_color = 0, 0, 0
        self.components = []

    def add_component(self, component):
        self.components.append(component)

    def update(self):
        for component in self.components:
            if hasattr(component, 'update'):
                component.update()

    def draw(self, screen):
        screen.fill(self.bg_color)
        for component in self.components:
            if hasattr(component, 'draw'):
                component.draw(screen)
        pygame.display.flip()

    def init(self):
        for component in self.components:
            if hasattr(component, 'init'):
                    component.init()

    def tick(self):
        screen = pygame.display.set_mode(self.size)
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            self.update()
            self.draw(screen)
            pygame.time.delay(100)


def main():
    # TODO: Initialize pygame resources
    game = RacingGamingClient()
    game.init_pygame_resources()

    # TODO: Initialize communications server

    # TODO: construct objects (matrix + car)
     ## create car

     ## create matrix
    game.add_component(matrix)

    # TODO: initialize objects
    game.init()

    # move to main game loop:
    game.tick()


if __name__ == '__main__':
    main()