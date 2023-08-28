from rose.common import actions, config


class Player(object):
    def __init__(self, name, car, lane):
        """
        Creates a new Driver object.
        Args:
            name (str): The unique name of the driver for display.
            car (int): A number from 0 to 3, representing the car type.
            lane (int): The initial lane number, between 0 and the maximum
                lane.

        Attributes:
            x (int, optional): The X-coordinate of the driver. Starts in the
                middle of the lane.
            y (int, optional): The Y-coordinate of the driver. Starts at 2/3 of
                the screen height.
            action (str, optional): The current driver action. Defaults to
                'none'.
            response_time (float, optional): The duration the driver takes to
                react. Starts as None.
            score (int, optional): The driver's current score. Begins at 0.
        """
        self.name = name
        self.car = car
        self.lane = lane
        self.x = None
        self.y = None
        self.action = None
        self.response_time = None
        self.score = None
        self.reset()

    # Game state interface

    def update(self):
        """Go to the next game state"""

    def reset(self):
        self.x = self.lane * config.cells_per_player + 1  # | |0| | |1 | |
        self.y = config.matrix_height // 3 * 2  # 1/3 of track
        self.action = actions.NONE
        self.response_time = None
        self.score = 0

    def in_lane(self):
        current_lane = self.x // config.cells_per_player
        return current_lane == self.lane

    def __cmp__(self, other):
        x = self.score
        y = other.score
        return (x > y) - (x < y)

    def __lt__(self, other):
        return self.score < other.score

    def state(self):
        """Return read only serialize-able state for sending to client"""
        return {
            "name": self.name,
            "car": self.car,
            "x": self.x,
            "y": self.y,
            "lane": self.lane,
            "score": self.score,
        }
