"""
This driver like to switch lanes even when it does not need to, prefering right
turn.
"""
from rtp.common import obstacles, actions

server_address = "localhost"
driver_name = "Zig Zag"

def drive(world):
    def valid_move(pos):
        try:
            obstacle = world.get_obstacle(pos)
        except IndexError:
            return False
        return obstacle in (obstacles.NONE, obstacles.PENGUIN)

    print 'POSITION: x=%s y=%s' % (world.car.x, world.car.y)

    # y = 0 is the top raw in the board
    # x = 0 is the leff lane

    # Check cell above the car (y-1)
    up = world.car.x, world.car.y - 1
    if valid_move(up):
        if world.get_obstacle(up) == obstacles.PENGUIN:
            print 'PICK'
            return actions.PICKUP
        else:
            print 'NONE'
            return actions.NONE

    # Check cell above and right
    right = world.car.x + 1, world.car.y - 1
    if valid_move(right):
        print 'RIGHT'
        return actions.RIGHT

    # Check cell above and left
    left = world.car.x + -1, world.car.y - 1
    if valid_move(left):
        print 'LEFT'
        return actions.LEFT

    print 'JUMP'
    return actions.JUMP
