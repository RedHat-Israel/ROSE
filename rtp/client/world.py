## The WORLD ##
class world(object):
    def __init__(self, matrix):
        self._m = matrix

    def watch_item_in_cell(self, pos):
        return self._m.get_obstacle(pos[0], pos[1])
