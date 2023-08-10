"""
This driver does not do any action.
"""
from rose.common import obstacles, actions  # NOQA

driver_name = "me"
bad = [obstacles.BIKE, obstacles.BARRIER, obstacles.TRASH]
good = [obstacles.WATER, obstacles.PENGUIN, obstacles.CRACK]
better = [obstacles.PENGUIN, obstacles.CRACK]
best = [obstacles.NONE, obstacles.PENGUIN]


def betterlane(world, x, y, lane):
    obstacle = world.get((x, y - 1))
    if lane == 0:
        if world.get((x - 1, y - 2)) in good and world.get((x - 1, y - 1)) in best and world.get(
                (x, y - 3)) != obstacles.PENGUIN:
            return actions.LEFT
        elif world.get((x + 1, y - 2)) in good and world.get((x + 1, y - 1)) in best and world.get(
                (x, y - 3)) != obstacles.PENGUIN:
            return actions.RIGHT
        elif world.get((x, y - 1)) in bad:
            for i in range(3, 6):
                if world.get((x - 1, y - i)) in good and world.get((x + 1, y - i)) != obstacles.PENGUIN:
                    return actions.LEFT
                else:
                    return actions.RIGHT
        else:
            return actions.NONE
    if lane == 1:
        if world.get((x - 1, y - 1)) in best and world.get((x, y - 2)) not in good:
            return actions.LEFT
        else:
            return actions.NONE
    if lane == 2:
        if world.get((x + 1, y - 1)) in best and world.get((x, y - 2)) not in good:
            return actions.RIGHT
        else:
            return actions.NONE


def drive(world):
    x = world.car.x
    y = world.car.y
    obstacle = world.get((x, y - 1))
    if x == 1 or x == 4:
        lane = 0  # 0=in middle, 1=in right, 2= in left
    elif x == 2 or x == 5:
        lane = 1
    else:
        lane = 2
    if obstacle == obstacles.PENGUIN:
        return actions.PICKUP
    if obstacle == obstacles.CRACK:
        if lane < 2 and world.get((x - 1, y - 2)) == obstacles.PENGUIN:
            return actions.LEFT
        elif lane % 2 == 0 and world.get((x + 1, y - 2)) in obstacles.PENGUIN:
            return actions.RIGHT
        else:
            return actions.JUMP
    if obstacle == obstacles.WATER:
        if lane < 2 and world.get((x - 1, y - 2)) in better:
            return actions.LEFT
        elif lane % 2 == 0 and world.get((x + 1, y - 2)) in better:
            return actions.RIGHT
        else:
            return actions.BRAKE

    if obstacle in bad:
        if lane == 0:
            return betterlane(world, x, y, lane)
        if lane == 1:
            return actions.LEFT
        if lane == 2:
            return actions.RIGHT
    return betterlane(world, x, y, lane)
