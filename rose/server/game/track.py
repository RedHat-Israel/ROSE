import random

from common import config, obstacles


class Track(object):
    def __init__(self, is_track_random=False):
        self._matrix = None
        self.is_track_random = is_track_random
        self.reset()

    # Game state interface

    def update(self):
        """Go to the next game state"""
        self._matrix.pop()
        self._matrix.insert(0, self._generate_row())

    def state(self):
        """Return read only serialize-able state for sending to client"""
        items = []
        for y, row in enumerate(self._matrix):
            for x, obs in enumerate(row):
                if obs != obstacles.NONE:
                    items.append({"name": obs, "x": x, "y": y})
        return items

    def matrix(self):
        """Return the track matrix"""
        return self._matrix

    # Track interface

    def get(self, x, y):
        """Return the obstacle in position x, y"""
        return self._matrix[y][x]

    def set(self, x, y, obstacle):
        """Set obstacle in position x, y"""
        self._matrix[y][x] = obstacle

    def clear(self, x, y):
        """Clear obstacle in position x, y"""
        self._matrix[y][x] = obstacles.NONE

    def reset(self):
        self._matrix = [
            [obstacles.NONE] * config.matrix_width for x in range(config.matrix_height)
        ]

    # Private

    def _generate_row(self):
        """
        Generates new row with obstacles

        Try to create fair but random obstacle stream. Each player get the same
        obstacles, but in different cells if 'is_track_random' is True.
        Otherwise, the tracks will be identical.
        """

        # Create initial empty row
        row = [obstacles.NONE] * config.matrix_width

        # Get a random obstacle
        obstacle = obstacles.get_random_obstacle()

        if self.is_track_random:
            for lane in range(config.max_players):
                # Get a random cell for each player
                cell = random.choice(range(0, config.cells_per_player))

                row[cell + lane * config.cells_per_player] = obstacle
        else:
            # Get a random cell, and use it for all players
            cell = random.choice(range(0, config.cells_per_player))

            for lane in range(config.max_players):
                row[cell + lane * config.cells_per_player] = obstacle

        return row
