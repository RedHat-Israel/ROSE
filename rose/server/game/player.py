from common import config, actions


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
        self.URL = ""
        self.lane = lane
        self.x = None
        self.y = None
        self.action = None
        self.httperror = None
        self.response_time = None
        self.score = None
        self.pickups = None
        self.misses = None
        self.hits = None
        self.breaks = None
        self.jumps = None
        self.collisions = None
        self.reset()

    def reset(self):
        self.x = self.lane * config.cells_per_player + 1  # | |0| | |1 | |
        self.y = config.matrix_height // 3 * 2  # 1/3 of track
        self.action = actions.NONE
        self.response_time = None
        self.score = 0
        self.pickups = 0
        self.misses = 0
        self.hits = 0
        self.breaks = 0
        self.collisions = 0
        self.jumps = 0

    def __cmp__(self, other):
        x = self.score
        y = other.score
        return (x > y) - (x < y)

    def __lt__(self, other):
        return self.score < other.score

    def in_lane(self):
        current_lane = self.x // config.cells_per_player
        return current_lane == self.lane

    def state(self):
        """Return read only serialize-able state for sending to client"""
        return {
            "name": self.name,
            "car": self.car,
            "x": self.x,
            "y": self.y,
            "action": self.action,
            "response_time": self.response_time,
            "error": self.httperror,
            "lane": self.lane,
            "score": self.score,
            "pickups": self.pickups,
            "misses": self.misses,
            "hits": self.hits,
            "breaks": self.breaks,
            "jumps": self.jumps,
            "collisions": self.collisions,
        }
