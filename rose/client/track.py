from rose.common import config, obstacles
import component


class Track(component.Component):

    def __init__(self):
        self._track = {}

    # Component interface

    def update(self, info):
        self._track = {(obs["x"], obs["y"]): obs["name"] for obs in info["track"]}

    # Track interface

    def get(self, x, y):
        """ Return the obstacle in position x, y """
        self._validate_pos(x, y)
        return self._track.get((x, y), obstacles.NONE)

    # Private

    def _validate_pos(self, x, y):
        if x < 0 or x > config.matrix_width - 1:
            raise IndexError('x out of range: 0-%d', config.matrix_width - 1)
        if y < 0 or y > config.matrix_height - 1:
            raise IndexError('y out of range: 0-%d', config.matrix_height - 1)
