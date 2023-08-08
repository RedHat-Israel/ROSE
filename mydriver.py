import constans
from rose.common import obstacles, actions  # NOQA

driver_name = "Michael Schumacher"

def generate_paths(x, y):
    paths = []
    for dy1 in range(1, 4):  # Moving upward
        for dx1 in range(-1, 2):  # Moving diagonally
            for dy2 in range(1, 4):  # Moving upward
                for dx2 in range(-1, 2):  # Moving diagonally
                    if dy1 != dy2:  # Ensure different y values
                        path = [(x + dx1, y - dy1), (x + dx2, y - dy2), (x, y)]
                        paths.append(path)
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