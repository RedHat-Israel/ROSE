import random
import matrix_config
import os

class Matrix():
    def __init__(self):
        self.matrix = [[matrix_config.EMPTY for x in xrange(matrix_config.WIDTH)]
                       for x in xrange(matrix_config.HEIGHT)]
        self.__generate_obstacles()

    def __generate_obstacles(self):
        """
        Generates obstacles for __init__
        """

        obstacles = 0
        while obstacles < matrix_config.NUMBER_OF_OBSTACLES:
            x = random.randint(0, matrix_config.WIDTH - 1)
            y = random.randint(0, matrix_config.HEIGHT - 1)

            if self.is_legal_obstacle_placement(x, y):
                self.matrix[y][x] = random.choice(matrix_config.OBSTACLES.values())
                obstacles += 1

    def is_legal_obstacle_placement(self, x, y):
        """
        Checks if x and y are legal
        """

        if y == 0:
            return self.check_below(x, y)
        elif y == matrix_config.HEIGHT - 1:
            return self.check_above(x, y)
        else:
            return self.check_above(x, y) and self.check_below(x, y)

    def check_below(self, x, y):
        return self.matrix[y + 1][x] == matrix_config.EMPTY

    def check_above(self, x, y):
        return self.matrix[y - 1][x] == matrix_config.EMPTY

    def check_right(self, x, y):
        return self.matrix[y][x+1] == matrix_config.EMPTY

    def check_left(self, x, y):
        return self.matrix[y][x-1] == matrix_config.EMPTY

    def print_matrix(self):
        for i in self.matrix:
            print i

    def get_obstacle(self, x, y):
        """
        Return the obstacle in location x, y
        """
        return self.matrix[y][x]

    def __generate_row(self):
        """
        Generates new row with obstacle
        """

        _counter = 0
        _tmp_list = []
        for i in self.matrix[0]:
            if i == matrix_config.EMPTY:
                _tmp_list.insert(_counter, random.choice(
                    matrix_config.OBSTACLES_FOR_NEXT_ROW.values())
                )
            else:
                _tmp_list.insert(_counter, matrix_config.EMPTY)
            _counter += 1

        return _tmp_list

    def __update_matrix(self, row):
        """"
        Updates the current matrix with the new row
        """

        self.matrix.pop()
        self.matrix.insert(0, row)

    def next_row(self):
        _tmp_row = self.__generate_row()
        self.__update_matrix(_tmp_row)
        return _tmp_row


    def load_tiles(self):
        import pygame
        # self.obstacle_textures = []
        # for tile_tex_file in os.listdir(config.TILE_TEXTURE_FILES_DIR):
        #     self.obstacle_textures.append(pygame.image.load(tile_tex_file))

        self.road_textures = []
        for tile_tex_file in os.listdir(matrix_config.ROAD_TEXTURE_FILES):
            self.road_textures.append(pygame.image.load(os.path
            .join(matrix_config.ROAD_TEXTURE_FILES, tile_tex_file)))

    def init(self):
        self.load_tiles()

    def draw(self, screen):
        # draw road background:
        for i in range(matrix_config.HEIGHT):
            screen.blit(self.road_textures[i % len(self.road_textures)], (0, i * matrix_config
            .ROW_HEIGHT))


        # TODO: draw obstacles on top of road:

    def update(self):
        self.road_textures.insert(0, self.road_textures.pop())

if __name__ == '__main__':
    m = Matrix()
    m.generate_obstacles()
    m.print_matrix()

