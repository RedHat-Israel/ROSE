from rtp.common import obstacles, actions


def drive(your_car_location, world):
    '''
    This function should return the next ACTION for drive

    your_car_location - tuple of (x, y) -> x for raw, y for col.
                        (0, 0) is the uppest left edge.

    world - an object for getting info about the game world

        workd.watch_item_in_cell(pos)

            returns the obstacle in position pos
    '''
    def valid_move(pos):
        try:
            obstacle = world.watch_item_in_cell(pos)
        except IndexError:
            return False
        return obstacle in (obstacles.NONE, obstacles.PENGIUN)

    print 'POSITION: x=%s y=%s' % (your_car_location.x, your_car_location.y)

    # y = 0 is the uppest raw in the board
    # x = 0 is the leftest lane

    # check cell above the car (y-1)
    up = your_car_location.x, your_car_location.y - 1
    if valid_move(up):
        if world.watch_item_in_cell(up) == obstacles.PENGIUN:
            print 'PICK'
            return actions.PICKUP
        else:
            print 'NONE'
            return actions.NONE

    # check cell above and right
    right = your_car_location.x + 1, your_car_location.y - 1
    if valid_move(right):
        print 'RIGHT'
        return actions.RIGHT

    # check cell above and left
    left = your_car_location.x + -1, your_car_location.y - 1
    if valid_move(left):
        print 'LEFT'
        return actions.LEFT

    print 'JUMP'
    return actions.JUMP
