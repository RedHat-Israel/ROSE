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

    if x % 3 == 1:
        line = 'M'
    elif x % 3 == 0:
        line = 'L'
    elif x % 3 == 2:
        line = 'R'

    if obstacle in good_obs_lst:
        return good_obs_response(obstacle)


def good_obs_response(obstacle):
    if obstacle == obstacles.PENGUIN:
        return actions.PICKUP
    elif obstacle == obstacles.CRACK:
        return actions.JUMP
    elif obstacle == obstacles.WATER:
        return actions.BRAKE

def obstacle_response(obstacle, line, world):
    if obstacle == obstacles.NONE:
        return actions.NONE
    elif obstacle == obstacles.TRASH or obstacle == obstacles.BARRIER or obstacle == obstacles.BIKE:
        if line == 'R':
            return actions.LEFT
        elif line == 'L':
            return actions.RIGHT
        elif line == 'M':
            if not check_side_obs('R', world):
                return actions.RIGHT
            elif not check_side_obs('L', world):
                return actions.LEFT
    else:
        return actions.NONE


def check_side_obs(side, world):
    x = world.car.x
    y = world.car.y

    try:
        if side == 'R':
            obstacle = world.get((x - 1, y - 1))
        if side == 'L':
            obstacle = world.get((x + 1, y - 1))
    except IndexError:
        return False

    return obstacle != obstacles.PENGUIN
