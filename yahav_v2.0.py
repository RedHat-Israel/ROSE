import random

from rose.common import obstacles, actions  # NOQA

driver_name = f"Driver v2.0 #{random.randint(1, 100)}"

bad_side_obstacles = [obstacles.BARRIER, obstacles.BIKE, obstacles.CRACK, obstacles.TRASH, obstacles.WATER]
actions_for_obstacles = {"penguin": "pickup", "water": "brake", "crack": "jump"}
points_for_obstacles = {"penguin": 10, "water": 4, "crack": 5, "": 0, "trash": 0, "bike": 0, "barrier": 0}
good_obstacles = ["penguin", "water", "crack"]

total_points = 0


def get_points(obstacle):
    return points_for_obstacles[obstacle]


def dont_die(world):
    options = ["right", "left", "none"]
    x, y = world.car.x, world.car.y

    if x in (0, 3):
        options.remove("left")

    elif x in (2, 5):
        options.remove("right")

    next_obstacle = world.get((x, y - 1))
    if next_obstacle not in (obstacles.NONE, obstacles.PENGUIN):
        options.remove("none")

    if "right" in options:
        right_obstacle = world.get((x + 1, y - 1))
        if right_obstacle in bad_side_obstacles:
            options.remove("right")

    if "left" in options:
        left_obstacle = world.get((x - 1, y - 1))
        if left_obstacle in bad_side_obstacles:
            options.remove("left")

    return options


def get_lane_points(world, x):
    lane_obstacle = [world.get((x, y)) for y in range(world.car.y - 2, world.car.y - 4, -1)]

    points = 0
    for obstacle in lane_obstacle:
        if obstacle in good_obstacles:
            points += points_for_obstacles[obstacle]

    return points


def return_direction_when_barrier(x, y, world):
    if x == 0 or x == 3:
        return actions.RIGHT
    elif x == 2 or x == 5:
        return actions.LEFT
    rightobstacle = world.get((x + 1, y - 2))
    leftobstacle = world.get((x - 1, y - 2))
    if rightobstacle == obstacles.PENGUIN:
        return actions.RIGHT
    elif leftobstacle == obstacles.PENGUIN:
        return actions.LEFT
    elif rightobstacle == obstacles.CRACK:
        return actions.RIGHT
    elif leftobstacle == obstacles.CRACK:
        return actions.LEFT
    elif rightobstacle == obstacles.WATER:
        return actions.RIGHT
    elif leftobstacle == obstacles.WATER:
        return actions.LEFT
    else:
        return actions.LEFT


def get_action(world):
    options = dont_die(world)

    x, y = world.car.x, world.car.y

    next_obstacle = world.get((x, y - 1))
    # print(next_obstacle)
    if next_obstacle in actions_for_obstacles.keys():
        # print(actions_for_obstacles[next_obstacle])
        return actions_for_obstacles[next_obstacle]

    if x in range(3):
        x_range = range(3)
        plus_index = 0
    else:
        x_range = range(3, 6)
        plus_index = 3
    if x in (1, 4):
        next_obstacles = [world.get((x1, y - 2)) for x1 in x_range]
        for i, obstacle in enumerate(next_obstacles):
            x1 = i + plus_index
            next_obstacle = world.get((x1, y - 1))
            if next_obstacle in bad_side_obstacles:
                next_obstacles[i] = obstacles.NONE

        best_obstacle = max(next_obstacles, key=get_points)
        next_obstacle = world.get((x, y - 1))
        if get_points(best_obstacle) != 0 and get_points(best_obstacle) > get_points(next_obstacle):
            best_index = next_obstacles.index(best_obstacle) + plus_index
            if best_index < x:
                if "left" in options:
                    return "left"
            elif best_index > x:
                if "right" in options:
                    return "right"
            elif "none" in options:
                return "none"
    elif x in (0, 3):
        next_obstacles = [world.get((x1, y - 2)) for x1 in range(plus_index, plus_index + 2)]
        for i, obstacle in enumerate(next_obstacles):
            x1 = i + plus_index
            next_obstacle = world.get((x1, y - 1))
            if next_obstacle in bad_side_obstacles:
                next_obstacles[i] = obstacles.NONE
        best_obstacle = max(next_obstacles, key=get_points)
        next_obstacle = world.get((x, y - 1))
        if get_points(best_obstacle) != 0 and get_points(best_obstacle) > get_points(next_obstacle):
            best_index = next_obstacles.index(best_obstacle) + plus_index
            if best_index > x:
                if "right" in options:
                    return "right"
            elif "none" in options:
                return "none"

    elif x in (2, 5):
        next_obstacles = [world.get((x1, y - 2)) for x1 in range(plus_index + 1, plus_index + 3)]
        for i, obstacle in enumerate(next_obstacles):
            x1 = i + plus_index
            next_obstacle = world.get((x1, y - 1))
            if next_obstacle in bad_side_obstacles:
                next_obstacles[i] = obstacles.NONE

        best_obstacle = max(next_obstacles, key=get_points)
        next_obstacle = world.get((x, y - 1))
        if get_points(best_obstacle) != 0 and get_points(best_obstacle) > get_points(next_obstacle):
            best_index = next_obstacles.index(best_obstacle) + plus_index
            if best_index < x:
                if "left" in options:
                    return "left"
            elif "none" in options:
                return "none"

    if x in (0, 3):
        middle_lane_points = get_lane_points(world, x + 1)
        right_lane_points = get_lane_points(world, x + 2)
        left_lane_points = get_lane_points(world, x)

        if (middle_lane_points > left_lane_points or right_lane_points > left_lane_points) and "right" in options:
            return "right"

    elif x in (2, 5):
        middle_lane_points = get_lane_points(world, x - 1)
        left_lane_points = get_lane_points(world, x - 2)
        right_lane_points = get_lane_points(world, x)

        if (middle_lane_points > right_lane_points or left_lane_points > right_lane_points) and "left" in options:
            return "left"

    elif x in (1, 4):
        middle_lane_points = get_lane_points(world, x)
        left_lane_points = get_lane_points(world, x - 1)
        right_lane_points = get_lane_points(world, x + 1)

        if right_lane_points > middle_lane_points or left_lane_points > middle_lane_points:
            if right_lane_points > left_lane_points and "right" in options:
                return "right"
            elif "left" in options:
                return "left"
    if "none" in options:
        return "none"
    return random.choice(options)


def get_layer_points(x, world, total_points):
    if x < 3:
        x_range = range(3)
    else:
        x_range = range(3, 6)
    layer_obstacles = [world.get((x_, world.car.y - 1)) for x_ in x_range]

    for obstacle in layer_obstacles:
        if obstacle in good_obstacles:
            total_points += points_for_obstacles[obstacle]

    return total_points + 10


def drive(world):
    global total_points
    total_points = get_layer_points(world.car.x, world, total_points)
    action = get_action(world)
    options = dont_die(world)
    if action not in options and action not in actions_for_obstacles.values():
        print(action, options)
    # action = random.choice(dont_die(world))
    return action
