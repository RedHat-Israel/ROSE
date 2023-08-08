import constans
from rose.common import obstacles, actions  # NOQA

driver_name = "Michael Schumacher"

def bounds(world, x):
    if x == 3 or x == 0:
        return "Full L"
    if x == 5 or x == 2:
        return "Full R"

def check_lane(world, x):
    if 0 <= x <= 2:
        return 1
    if 3 <= x <= 5:
        return 2


def generate_paths(world, x, y):
    paths = []
    x_paths = [x, x - 1, x + 1]
    if bounds(world, x) == "Full L" and check_lane(world, x) == 1:
        x_paths.remove(x - 1)

    if bounds(world, x) == "Full R" and check_lane(world, x) == 2:
        x_paths.remove(x + 1)

    for x in x_paths:
        paths.append(((x, y - 1), (x, y - 2)))
    return paths

def calc_score_for_path(world, path):
    score = 0
    x, y = path[-1]  # Get the current position of the car

    try:
        obstacle = world.get((x, y - 1))
    except IndexError:
        return actions.NONE  # Don't move if out of bounds

    moves = []
    for loc in path:
        if obstacle == obstacles.NONE:
            score += 0
            moves.append(actions.NONE)
        elif obstacle == obstacles.PENGUIN:
            score += 10
            moves.append(actions.PICKUP)
        elif obstacle == obstacles.WATER:
            score += 4
            moves.append(actions.BRAKE)
        elif obstacle == obstacles.CRACK:
            score += 5
            moves.append(actions.JUMP)
        elif obstacle == obstacles.TRASH or obstacle == obstacles.BIKE or obstacle == obstacles.BARRIER:
            score -= 10
            moves.append(obstacles.BARRIER)
    # Check for collisions with lane owner
    if not (0 <= y < 10):
        score -= 10

    return score, moves

def find_best_path(world, x, y):
    paths = generate_paths(x, y)
    best_score = float('-inf')
    best_path = []
    moves = []
    for path in paths:
        score, move = calc_score_for_path(world, path)
        if score > best_score:
            best_score = score
            best_path = path
            moves = move
    return best_path, moves

def drive(world):
    x = world.car.x
    y = world.car.y
    best, moves = find_best_path(world, x, y)
    # Check for obstacles at the next position

    for loc in best:
        for move in moves:
            if move == obstacles.BARRIER:
                if loc[0] <= x:
                    return actions.LEFT
                elif loc[0] >= x:
                    return actions.RIGHT
            return move