from rose.common import obstacles, actions

driver_name = "Car_6"

def drive(world):
    x = world.car.x
    y = world.car.y

    try:
        obstacle = world.get((x, y - 1))
    except IndexError:
        pass
        # change once look farther.

    # add way to check line - using x?
    if x == 1 or x == 4:
        line = 'M'
    elif x == 0 or x == 3:
        line = 'L'
    elif x == 2 or x == 5:
        line = 'R'

    if obstacle == obstacles.NONE:
        return actions.NONE
    elif obstacle == obstacles.PENGUIN:
        return actions.PICKUP
    elif obstacle == obstacles.CRACK:
        return actions.JUMP
    elif obstacle == obstacles.WATER:
        return actions.BRAKE
    elif obstacle == obstacles.TRASH or obstacle == obstacles.BARRIER or obstacle == obstacles.BIKE:
        if line == 'R':
            return actions.LEFT
        elif line == 'L':
            return actions.RIGHT
        elif line == 'M':
            if not check_side_obs('R'):
                return actions.RIGHT
            elif not check_side_obs('L'):
                return actions.LEFT



def check_side_obs(side):
    x = world.car.x
    y = world.car.y

    try:
        if side == 'R':
            obstacle = world.get((x + 1 , y))
        if side == 'L':
            obstacle = world.get((x - 1 , y))
    except IndexError:
        return False

    return obstacle != obstacles.PENGUIN



