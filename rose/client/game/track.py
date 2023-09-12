class Track:
    def __init__(self, initial_track=None):
        """
        Initialize the track with the provided 2D array.

        :param initial_track: 2D array representing the initial state of the
        track.
        """
        if initial_track is None:
            initial_track = []
        self._track = initial_track

        self.max_x = len(self._track[0]) if self._track else 0
        self.max_y = len(self._track)

    # Track interface

    def get(self, x, y):
        """
        Return the action in position x, y.

        :param x: x-coordinate of the position.
        :param y: y-coordinate of the position.
        :return: The action at the specified position.
        """
        self._validate_pos(x, y)
        return self._track[y][x]

    # Private

    def _validate_pos(self, x, y):
        """
        Validate if the provided x, y coordinates are within the bounds of the
        track.
        """
        if x < 0 or x >= self.max_x:
            raise IndexError(f"x out of range: 0-{self.max_x - 1}")
        if y < 0 or y >= self.max_y:
            raise IndexError(f"y out of range: 0-{self.max_y - 1}")
