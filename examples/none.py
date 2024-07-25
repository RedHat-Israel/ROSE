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

def score(obs):
    match obs:
        case obstacles.NONE:
            return 0
        case obstacles.PENGUIN:
            return 10
        case obstacles.WATER:
            return 5
        case obstacles.CRACK:
            return 4
        case obstacles.TRASH:
            return -10
        case obstacles.BIKE:
            return -10
        case obstacles.BARRIER:
            return -10
        case _:
            return 0

def new(cur_pos_x, cur_pos_y, obs, world, min_x, max_x):
        left = [world.get((cur_pos_x - 1, cur_pos_y - 1))]
        left.append(score(left[0]))
        print(f"Left lane: {left}")

        right = [world.get((cur_pos_x + 1, cur_pos_y - 1))]
        right.append(score(right[0]))
        print(f"Right lane: {right}")

        middle = [world.get((cur_pos_x, cur_pos_y - 1))]
        middle.append(score(middle[0]))
        print(f"Middle lane: {middle}")

        best_lane = better(left, right, middle)
        if best_lane == left:
            return actions.LEFT
        elif best_lane == right:
            return actions.RIGHT
        else:  # best_lane == middle
            return actions.NONE

def better(left, right, middle):
    higher = max(left[1], right[1], middle[1])
    if higher == left[1]:
        return left
    elif higher == right[1]:
        return right
    elif higher == middle[1]:
        return middle
    else:
        print('fgbfrewrererg')
        return middle


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
            return new(cur_pos_x, cur_pos_y, obs, world, min_x, max_x)
        case obstacles.BIKE:
            return new(cur_pos_x, cur_pos_y, obs, world, min_x, max_x)
        case obstacles.BARRIER:
            return new(cur_pos_x, cur_pos_y, obs, world, min_x, max_x)
        case _:
            return actions.NONE
