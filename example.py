from components.matrix_config import NONE, JUMP, RIGHT, LEFT, PICKUP, \
    PENGIUN, EMPTY


def drive(car, matrix):
    '''
    This function should return the next ACTION for drive
    '''
    def valid_move(m, x, y):
        try:
            print m.get_obstacle(x, y)
            return m.get_obstacle(x, y) in (EMPTY, PENGIUN)
        except IndexError:
            return False

    x, y = car.lane, car.speed  # getting current location on map
    print 'POSITION: x=%s y=%s' % (x, y)

    # y = 0 is the uppest raw in the board
    # x = 0 is the leftest lane

    if valid_move(matrix, x, y - 1):  # check cell above the car (y-1)
        if matrix.get_obstacle(x, y - 1) == PENGIUN:
            print 'PICK'
            return PICKUP
        else:
            print 'NONE'
            return NONE
    elif valid_move(matrix, x + 1, y - 1):  # check cell above and right
        print 'RIGHT'
        return RIGHT
    elif valid_move(matrix, x - 1, y - 1):  # check cell above and left
        print 'LEFT'
        return LEFT
    else:
        print 'JUMP'
        return JUMP
