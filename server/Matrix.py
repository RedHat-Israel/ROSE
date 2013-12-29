import random
import config
import os

class Matrix():
    def __init__(self):
        self.matrix = [[config.EMPTY for x in xrange(config.WIDTH)]
                       for x in xrange(config.HEIGHT)]

    def generate_obstacles(self):
        obstacles = 0
        while obstacles < config.NUMBER_OF_OBSTACLES:
            x = random.randint(0, config.WIDTH - 1)
            y = random.randint(0, config.HEIGHT - 1)

            if self.is_legal_obstacle_placement(x,y):
                self.matrix[y][x] = random.choice(config.OBSTACLES.values())
                obstacles += 1

    def is_legal_obstacle_placement(self, x, y):
        if y == 0:
            return self.check_below(x, y)
        elif y == config.HEIGHT - 1:
            return self.check_above(x, y)
        else:
            return self.check_above(x, y) and self.check_below(x, y)

    def check_below(self, x, y):
        return self.matrix[y + 1][x] == config.EMPTY

    def check_above(self, x, y):
        return self.matrix[y - 1][x] == config.EMPTY

    def print_matrix(self):
        for i in self.matrix:
            print i

    def load_tiles(self):
        import pygame
        self.obstacle_textures = []
        for tile_tex_file in os.listdir(config.TILE_TEXTURE_FILES_DIR):
            self.obstacle_textures.append(pygame.image.load(tile_tex_file))

        self.road_textures = []
        for tile_tex_file in os.listdir(config.ROAD_TEXTURE_FILES):
            self.road_textures.append(pygame.image.load(tile_tex_file))

    def init(self):
        self.generate_obstacles()
        self.load_tiles()

    def draw(self, screen):

        # draw road background:
        for i in config.HEIGHT:
            screen.blit(self.road_textures[i % 3], (0, i * config.ROW_HEIGHT))

        # TODO: draw obstacles on top of road:

if __name__ == '__main__':
    m = Matrix()
    m.generate_obstacles()
    m.print_matrix()