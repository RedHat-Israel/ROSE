from none import *


def find_lane(cur_pos_x, cur_pos_y):
    min_x, max_x = 0, 2
    return min_x, max_x


def count(points, op):
    sum_points = 0
    for i in points[op]:
        sum_points += i

    return sum_points


def merge(op_1, op_2, op_3, points):

    if op_1 == 'no' and op_2 == 'no' and op_3 == 'no':
        return ['no']

    if op_1 == 'no' and op_2 == 'no' and op_3 != 'no':
        return [op_3]

    if op_1 == 'no' and op_2 != 'no' and op_3 == 'no':
        return [op_2]

    if op_1 != 'no' and op_2 == 'no' and op_3 == 'no':
        return [op_1]

    if count(points, op_1) >= count(points, op_2):
        if count(points, op_1) >= count(points, op_3):
            return [op_1]
        else:
            return [op_3]
    elif count(points, op_2) >= count(points, op_3):
        return [op_2]
    else:
        return [op_3]







def priorities(lane, step, points, bord, cur_pos_x , cur_pos_y):
    min_x, max_x = find_lane(cur_pos_x, cur_pos_y)
    if lane > max_x or lane < min_x:
        return ['no']
    if step <= 0:
        return ["finish"]

    points += (bord[cur_pos_x][cur_pos_y])

    R = ['r'] + priorities(lane+1, step-1, points, bord, cur_pos_x +1, cur_pos_y +1)
    M = ['m'] + priorities(lane, step - 1, points, bord, cur_pos_x, cur_pos_y +1)
    L = ['m'] + priorities(lane -1, step - 1, points, bord, cur_pos_x -1, cur_pos_y +1)

    return merge(R, M, L, points)



points =
bord = [[[-10], [+5], [+10]], [[+10], [0], [-10]]]
lane = 1
step = 1
cur_pos_x = 1
cur_pos_y = 0

print(priorities(lane, step, points, bord, cur_pos_x, cur_pos_y))


def pen(cur_pos_x, cur_pos_y, obs, world, min_x, max_x):
    if min_x < cur_pos_x < max_x:
        right_next_obs = world.get((cur_pos_x + 1, cur_pos_y - 2))
        left_next_obs = world.get((cur_pos_x - 1, cur_pos_y - 2))
        right_obs = world.get((cur_pos_x + 1, cur_pos_y - 1))
        left_obs = world.get((cur_pos_x + 1, cur_pos_y - 1))
        if right_next_obs == obstacles.PENGUIN and right_obs not in [obstacles.BIKE, obstacles.TRASH,
                                                                     obstacles.BARRIER]:
            return actions.RIGHT
        elif left_next_obs == obstacles.PENGUIN and left_obs not in [obstacles.BIKE, obstacles.TRASH,
                                                                     obstacles.BARRIER]:
            return actions.LEFT
        elif right_obs == obstacles.PENGUIN:
            return actions.RIGHT, actions.PICKUP
        elif left_obs == obstacles.PENGUIN:
            return actions.LEFT, actions.PICKUP
        else:
            return actions.NONE
    return actions.NONE

