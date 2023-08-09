from rose.common import obstacles, actions  # NOQA

driver_name = "Emily"

scores = {obstacles.NONE: 0, obstacles.PENGUIN: 10, obstacles.WATER: 4, obstacles.CRACK: 5, obstacles.TRASH: -10, obstacles.BIKE: -10, obstacles.BARRIER: -10}

ACTIONS_ob = {obstacles.NONE: False, obstacles.PENGUIN: actions.PICKUP, obstacles.WATER: actions.BRAKE, obstacles.CRACK: actions.JUMP, obstacles.TRASH: False, obstacles.BIKE: False, obstacles.BARRIER: False}


def check_lane(x):
    if 0 <= x <= 2:
        return 1
    if 3 <= x <= 5:
        return 2

def bounds_x(x):
    if check_lane(x) == 1:
        return [0,1,2]
    if check_lane(x) == 2:
        return [3,4,5]


def generate_paths(x, y):
    paths = {}
    x_paths = bounds_x(x)
    for cx in x_paths:
        paths[(cx, y - 2)] = []
        if x - 1 < min(x_paths):
            try:
                del paths[(max(x_paths), y - 2)]
            except:
                pass
        if x + 1 > max(x_paths):
            try:
                del paths[(min(x_paths), y - 2)]
            except:
                pass

    for cx in x_paths:
        for path in paths.keys():
            paths[path].append((cx, y - 3))
            if path[0] - 1 < min(x_paths):
                try:
                    paths[path].remove((max(x_paths), y - 3))
                except:
                    pass
            if path[0] + 1 > max(x_paths):
                try:
                    paths[path].remove((min(x_paths), y - 3))
                except:
                    pass
    return paths

def calc_score_for_path(world, paths):
    current_score = 0
    highest_score = 0
    x = world.car.x
    x_paths = bounds_x(x)
    best_path = x_paths[1]
    for path in paths.keys():
        obstacle_y_1 = world.get(path)
        current_score = scores[obstacle_y_1]
        for y2_path in paths[path][1::]:
            obstacle_y_2 = world.get(y2_path)
            current_score += scores[obstacle_y_2]
        if current_score > highest_score:
            highest_score = current_score
            best_path = path[0]
    if x == best_path:
        action = actions.NONE
    elif x < best_path and x + 1 in x_paths:
        action = actions.RIGHT
    elif x > best_path and x - 1 in x_paths:
        action = actions.LEFT

    print(best_path)
    return action

def drive(world):
    x = world.car.x
    y = world.car.y

    action = calc_score_for_path(world, generate_paths(x, y))
    next_obstacle = world.get((x, y - 1))

    if ACTIONS_ob[next_obstacle]:
        return ACTIONS_ob[next_obstacle]
    else:
        return action