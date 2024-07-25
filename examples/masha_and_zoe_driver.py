from rose.common import obstacles, actions

driver_name = "Zoe and Masha"
running = True

# Define valid lane ranges based on the starting position
def get_lane_range(starting_position):
    if starting_position == 1:
        return 0, 2
    elif starting_position == 4:
        return 3, 5
    else:
        # Default to a range that includes only the starting position if not 1 or 4
        return starting_position, starting_position

def run(cur_pos_x, cur_pos_y, obs, world, min_x, max_x):
    if cur_pos_x == min_x:
        return actions.RIGHT
    elif cur_pos_x == max_x:
        return actions.LEFT
    else:
        if min_x < cur_pos_x < max_x:
            if obs != obstacles.PENGUIN and obs != obstacles.NONE:
                next_obs = world.get((cur_pos_x - 1, cur_pos_y - 1))
                if next_obs == obstacles.PENGUIN or next_obs == obstacles.NONE:
                    return actions.LEFT
                else:
                    return actions.NONE
            else:
                next_obs = world.get((cur_pos_x + 1, cur_pos_y - 1))
                if next_obs == obstacles.PENGUIN or next_obs == obstacles.NONE:
                    return actions.RIGHT
                else:
                    return actions.NONE
        else:
            return actions.NONE

def drive(world):
    cur_pos_x = world.car.x
    cur_pos_y = world.car.y

    # Determine the lane range based on the starting position
    min_x, max_x = get_lane_range(cur_pos_x)

    obs = world.get((cur_pos_x, cur_pos_y - 1))
    match obs:
        case obstacles.NONE:
            return actions.NONE
        case obstacles.PENGUIN:
            return actions.PICKUP
        case obstacles.WATER:
            return actions.BRAKE
        case obstacles.CRACK:
            return actions.JUMP
        case obstacles.TRASH:
            return run(cur_pos_x, cur_pos_y, obs, world, min_x, max_x)
        case obstacles.BIKE:
            return run(cur_pos_x, cur_pos_y, obs, world, min_x, max_x)
        case obstacles.BARRIER:
            return run(cur_pos_x, cur_pos_y, obs, world, min_x, max_x)
        case _:
            return actions.NONE
