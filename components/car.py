import matrix_config as config
import os


class Car():
    def __init__(self, id, x, y):
        self._location = (x, y)
        self._texture = os.path.join(
            config.CAR_TEXTURE_FILES_DIR, config.CAR_TEXTURE_FILE
        ) + str(id)

    def draw(self, screen):
        screen.blit(
            self.texture,
            self._location[1]*config.TILEHEIGHT,
            self._location[0].config.TILEHEIGHT
        )
