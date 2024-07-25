import random
import ast
from rose.common import config, obstacles
import os


class Track(object):
    def __init__(self):
        self._matrix = None
        self.file_read = None
        self.line_read = None

        self.line_write = None

        self.reset()

    # Game state interface

    def update(self):
        """Go to the next game state"""
        self._matrix.pop()
        if config.track_read_mode:
            new_row = self._get_row_from_file()
        else:
            new_row = self._generate_row()
        if config.track_write_mode:
            self.save_line_to_file(new_row)

        self._matrix.insert(0, new_row)

    def state(self):
        """Return read only serialize-able state for sending to client"""
        items = []
        for y, row in enumerate(self._matrix):
            for x, obs in enumerate(row):
                if obs != obstacles.NONE:
                    items.append({"name": obs, "x": x, "y": y})
        return items

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

        # If server in reader mode, this code will reset variables of read file
        if config.track_read_mode:
            # if file is already opened, do not open it again
            if self.file_read is None:
                self.file_read = open(config.track_file_name_read).readlines()
            self.line_read = 1

        # If file already exist, this code will remove it
        # to start new file for the new map.
        if config.track_write_mode:
            if os.path.exists(config.track_file_name_write):
                # os.remove(config.track_file_name_write)

                file = open(config.track_file_name_write, "w")
                file.write("[\n")
                self.line_write = 0


    # Private

    def _generate_row(self):
        """
        Generates new row with obstacles

        Try to create fair but random obstacle stream. Each player get the same
        obstacles, but in different cells if 'is_track_random' is True.
        Otherwise, the tracks will be identical.
        """

        row = [obstacles.NONE] * config.matrix_width
        obstacle = obstacles.get_random_obstacle()
        if config.is_track_random:
            for lane in range(config.max_players):
                low = lane * config.cells_per_player
                high = low + config.cells_per_player
                cell = random.choice(range(low, high))
                row[cell] = obstacle
        else:
            cell = random.choice(range(0, config.cells_per_player))
            for lane in range(config.max_players):
                row[cell + lane * config.cells_per_player] = obstacle
        return row

    def _get_row_from_file(self):
        """
        Gets row from file(json) of map.
        Function will get row by number of line to read(self.line_read) and increase value of
        this variable by one.
        If function get last line from file, value of self.line_read will set to 0.

        example:
        row in file - ['', '', 'trash', 'trash', '', ''],
        row returned - ['', '', 'trash', 'trash', '', '']
        """
        if self.line_read < config.max_line:
            st = self.file_read[self.line_read][:-2]
        else:
            st = self.file_read[self.line_read]



        row = ast.literal_eval(st)
        self.line_read += 1

        if self.line_read > config.max_line:
            self.line_read = 0

        return row

    def save_line_to_file(self, row):
        """
        Function will append current row to file(json structure).
        file path is config.track_file_name_write

        example of row - ['', '', 'trash', 'trash', '', '']
        example of row in file - ["", "", "trash", "trash", "", ""],
        """

        with open(config.track_file_name_write, "a") as outfile:
            self.line_write += 1
            outfile.write(str(row).replace("'", '"'))
            if self.line_write == config.max_line:
                outfile.write("\n]")
            else:
                outfile.write(",\n")

