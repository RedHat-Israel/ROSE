""" Game obstacles """

import random

NONE    = ""         # NOQA
CRACK   = "crack"    # NOQA
TRASH   = "trash"    # NOQA
PENGUIN = "penguin"  # NOQA
BIKE    = "bike"     # NOQA
WATER   = "water"    # NOQA
BARRIER = "barrier"  # NOQA

ALL = (NONE, CRACK, TRASH, PENGUIN, BIKE, WATER, BARRIER)


def get_random_obstacle():
    obstacle = ''
    num = random.randint(0, 100)
    if num < 50:
        obstacle = PENGUIN
    else:
        obstacle = random.choice(ALL)
    return obstacle
    #return random.choice(ALL)
