import components.matrix_config as config


def drive(your_car_location, world):
    '''
    This function should return the next ACTION for drive

    your_car_location - tuple of (x, y) -> x for raw, y for col.
                        (0, 0) is the uppest left edge.

    check_for_obstacle_func - The func gets x, y cordination and returns what
                              exists on that cell in the world.
                              for example:
                              your_car_location.x, your_car_location.y - 1
                              detemine what exists in-front of your car
    '''
    def valid_move(i):
        try:
            return i in (config.EMPTY, config.PENGIUN)
        except IndexError:
            return False

    print 'POSITION: x=%s y=%s' % (your_car_location.x, your_car_location.y)

    # y = 0 is the uppest raw in the board
    # x = 0 is the leftest lane

    # check cell above the car (y-1)
    if valid_move(world.watch_item_in_cell(your_car_location.x,
                                           your_car_location.y - 1)):
        if world.watch_item_in_cell(your_car_location.x,
                                    your_car_location.y) == config.PENGIUN:
            print 'PICK'
            return config.PICKUP
        else:
            print 'NONE'
            return config.NONE

    # check cell above and right
    elif valid_move(world.watch_item_in_cell(
                    your_car_location.x + 1,
                    your_car_location.y - 1)):
        print 'RIGHT'
        return config.RIGHT

    # check cell above and left
    elif valid_move(world.watch_item_in_cell(
                    your_car_location.x - 1,
                    your_car_location.y - 1)):
        print 'LEFT'
        return config.LEFT

    else:
        print 'JUMP'
        return config.JUMP
