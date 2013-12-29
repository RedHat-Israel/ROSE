import matrix_config 
import os
import car_config

class Car():


    def __init__(self, id, x, y):
        self._location = (x, y)
        self._texture = os.path.join(
            car_config.CAR_TEXTURE_FILES_DIR, car_config.CAR_TEXTURE_FILE
        ) + str(id)

    def draw(self, screen):
        screen.blit(
            self.texture,
            self._location[1]*matrix_config.TILEHEIGHT,
            self._location[0]*matrix_config.TILEHEIGHT
        )
