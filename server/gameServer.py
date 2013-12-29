from components import matrix_config
import matrix


class GameServer:
    """
    Implements the server for the car race
    """

    def __init__(self):
        self.matrix = matrix()
        self.lives = [3] * matrix_config.NUMBER_OF_PLAYERS

    def do(self, car_num, action, x, y):
        """
        Returns the new position of each car
        Args:
            * car_num - num between 1-4
            * action - the action to preform
            * x - latitude
            * y - altitude
        Available actions are:
            - Move forward
            - Move right
            - Move left
            - Jump
            - Pick (star)
        """
        if action == matrix_config.MOVE['FORWARD']:
            if self.matrix.check_above(x, y): # can move forward
                return x, y-1
            else:
                return self._dec_life_and_return(car_num, x, y)
        elif action == matrix_config.MOVE['RIGHT']:
            if self.matrix.check_right:  # can move right
                return x+1, y
            else:
                return self._dec_life_and_return(car_num, x, y)
        elif action == matrix_config.MOVE['LEFT']:
            if self.matrix.check_left:  # can move left
                return x-1, y
            else:
                return self._dec_life_and_return(car_num, x, y)
        elif action == matrix_config.ACTIONS['PICK']:
            self._pick(car_num, x, y)
            return x, y  # don't check location
        elif action == matrix_config.ACTIONS['JUMP']:
            return x, y-2
        else:  # unknown action - don't move
            return x, y

    def _pick(self, car_num, x, y):
        """
        Increase life for a car if there is a star there
        Args:
            * car_num - num between 1-4
            * x - latitude
            * y - altitude
        """
        if self.matrix.get_obstacle(x, y) == matrix_config.OBSTACLES['STAR']:
            self._inc_life()

    def _inc_life(self, car_num):
        """
        Increase number of lives
        """
        self.lives[car_num-1] += 1

    def _dec_life(self, car_num):
        """
        Decrease number of lives
        """
        self.lives[car_num-1] -= 1

    def _is_alive(self, car_num):
        """
        Returns True if the car is still alive
        """
        return self.lives[car_num-1] > 0

    def _dec_life_and_return(self, car_num, x, y):
        """
        Decrease number of life and return next position
        """
        self._dec_life(car_num)
        if self._is_alive(car_num):
            return x, y
        else:  # dead
            return -1, -1