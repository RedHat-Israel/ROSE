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



    if obstacle == obstacles.NONE:
        return actions.NONE
    elif obstacle == obstacles.PENGUIN:
        return actions.PICKUP
    elif obstacle == obstacles.CRACK:
        return actions.JUMP
    elif obstacle == obstacles.WATER:
        return actions.BRAKE
    elif obstacle == obstacles.TRASH:
        r

