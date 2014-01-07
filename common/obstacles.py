""" Game obstacles """

import random

NONE = -1
ALL = CRACK, TRASH, PENGIUN, BIKE, WATER, BARRIER = tuple(range(6))


def get_random_obstacle():
    return random.choice(ALL)
