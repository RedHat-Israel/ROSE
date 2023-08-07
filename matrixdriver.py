from rose.common import obstacles, actions
from variables import *

driver_name = "Car_6"


def drive(world):
    x = world.car.x
    y = world.car.y

    side_lines = side_lines_finder(x)
    line = line_finder(x)

    matrix = matrix_maker(world, side_lines)
    return pathfinder(matrix, line, world)


def line_finder(x):
    return x % 3

def side_lines_finder(x):
    if x >= 3:
        return [3, 4 , 5]
    else:
        return [0, 1, 2]

def matrix_maker(world, side_lines):
    y = world.car.y
    matrix = []


    for col in range(1, 4):
        temp = []
        for row in side_lines:
            try:
                obstacle = world.get((row, y - col))
            except IndexError:
                obstacle = obstacles.NONE

            score = score_obs(obstacle)
            temp.append(score)
        matrix.append(temp)

    return matrix

def score_obs(obstacle):
    if obstacle in bad_obs_lst:
        return (bad_obs_score, bad_obs_score)
    else:
        if obstacle == obstacles.PENGUIN:
            return (penguin_gain_score, penguin_loss_score)
        elif obstacle == obstacles.WATER:
            return (water_gain_score, water_loss_score)
        elif obstacle == obstacles.CRACK:
            return (crack_gain_score, crack_loss_score)
    return (none_score, none_score)

def pathfinder(matrix, line, world):
    if line == 0:
        way1gain = matrix[0][0][0] + matrix[1][0][0]
        way2gain = matrix[0][1][1] + matrix[1][1][0]
        if way1gain > way2gain:
           return  obs_response(score_to_obs(world))
        elif way2gain > way1gain:
            return actions.RIGHT
        else:
            return actions.NONE

    elif line == 1:
        way1gain = matrix[0][0][1] + matrix[1][0][0]
        way2gain = matrix[0][1][0] + matrix[1][1][0]
        way3gain = matrix[0][2][1] + matrix[1][2][0]

        if way1gain > way2gain and way1gain > way3gain:
            return actions.LEFT
        elif way3gain > way1gain and way3gain > way2gain:
            return actions.RIGHT
        elif way2gain > way3gain and way2gain > way1gain:
            return obs_response(score_to_obs(world))
        else:
            return actions.NONE

    elif line == 2:
        if matrix[2][2][0] == -10:
            return actions.LEFT

        way3gain = matrix[0][2][0] + matrix[1][2][0]
        way2gain = matrix[0][1][1] + matrix[1][1][0]
        if way3gain > way2gain:
            return obs_response(score_to_obs(world))
        elif way2gain > way3gain:
            return actions.LEFT
        else:
            return actions.NONE
    return actions.NONE

def obs_response(obstacle):
    if obstacle == obstacles.PENGUIN:
        return actions.PICKUP
    elif obstacle == obstacles.CRACK:
        return actions.JUMP
    elif obstacle == obstacles.WATER:
        return actions.BRAKE
    else:
        return actions.NONE

def score_to_obs(world):
    # if obstacle_score == (water_gain_score, water_loss_score):
    #     return obstacles.WATER
    # elif obstacle_score == (crack_gain_score, crack_loss_score):
    #     return obstacles.CRACK
    # elif obstacle_score == (penguin_gain_score, penguin_loss_score):
    #     return obstacles.PENGUIN
    # elif obstacle_score == (bad_obs_score, bad_obs_score):
    #     return obstacles.BIKE
    # return obstacles.NONE
    x = world.car.x
    y = world.car.y

    try:
        return world.get((x, y - 1))
    except IndexError:
        return obstacles.NONE
