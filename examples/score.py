"""
This driver try to pick the action with the best score.
"""
import random
import itertools
from rtp.common import obstacles, actions

server_address = "localhost"
driver_name = "Score"

def drive(world):
    # Calculate the score for each action and collect the results
    x, y = world.car.x, world.car.y - 1  # Next row
    options = []
    check_forward(world, (x, y), options)
    check_turn(world, (x + 1, y), actions.RIGHT, options)
    check_turn(world, (x - 1, y), actions.LEFT, options)

    # Pick the action with the best score. If several actions have the best
    # score, pick one randomly.
    options.sort(reverse=True)
    print 'options:', options
    for k, g in itertools.groupby(options, lambda x: x[0]):
        best = list(g)
        score, action = random.choice(best)
        print 'score:', score, 'action:', action
        return action


# Scores:
#
# 6 - I can pick up a penguin *now*
# 5 - I can handle next obstacle and pick up a penguin later
# 4 - I can switch lane and pick up a penguin later
# 3 - I can handle next obstacle (none, water, crack)
# 2 - I can switch to a lane without a penguin
# 1 - I cannot handle next obstacle (bike, trash, barier)

def check_forward(world, (x, y), options):
    try:
        obstacle = world.get_obstacle((x, y))
        if obstacle == obstacles.PENGUIN:
            print 'check_forward obstacle:', obstacle, 'score: 6 action:', actions.PICKUP
            options.append((5, actions.PICKUP))
        elif obstacle in (obstacles.TRASH, obstacles.BARRIER, obstacles.BIKE):
            print 'check_forward obstacle:', obstacle, 'score: 1 action:', actions.NONE
            options.append((1, actions.NONE))
        else:
            score = 5 if penguin_ahead(world, (x, y - 1)) else 3
            if obstacle == obstacles.WATER:
                print 'check_forward obstacle:', obstacle, 'score:', score, 'action:', actions.BRAKE
                options.append((score, actions.BRAKE))
            elif obstacle == obstacles.CRACK:
                print 'check_forward obstacle:', obstacle, 'score:', score, 'action:', actions.JUMP
                options.append((score, actions.JUMP))
            elif obstacle == obstacles.NONE:
                print 'check_forward obstacle:', obstacle, 'score:', score, 'action:', actions.NONE
                options.append((score, actions.NONE))
    except IndexError:
        print 'check_forward obstacle: invalid', 'score: 4 action:', actions.NONE
        options.append((4, actions.NONE))


def check_turn(world, (x, y), action, options):
    # Can I switch to this lane?
    try:
        obstacle = world.get_obstacle((x, y))
    except IndexError:
        print 'check_turn: cannot switch to lane: %d' % x
        return  # No
    if obstacle not in (obstacles.NONE, obstacles.PENGUIN):
        print 'check_turn: obstacle:', obstacle, 'score: 1 action:', action
        options.append((1, action))
        return
    # I can switch, but how good is this lane?
    if penguin_ahead(world, (x, y - 1)):
        print 'check_turn:', 'penguin ahead in lane: %d' % x
        options.append((4, action))
    else:
        print 'check_turn:', 'no penguin ahead in lane: %d' % x
        options.append((2, action))


def penguin_ahead(world, (x, y)):
    while 1:
        try:
            obstacle = world.get_obstacle((x, y))
        except IndexError:
            return False
        if obstacle == obstacles.PENGUIN:
            return True
        if obstacle in (obstacles.TRASH, obstacles.BARRIER, obstacles.BIKE):
            return False
        y -= 1
