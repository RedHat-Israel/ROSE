## The WORLD ##
class world(object):
    def __init__(self, matrix):
        self._m = matrix

    def watch_item_in_cell(self, x, y):
        return self._m.get_obstacle(x, y)
