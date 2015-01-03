""" Game obstacles """

import random

ALL = NONE, CRACK, TRASH, PENGUIN, BIKE, WATER, BARRIER = tuple(range(-1, 6))


def get_random_obstacle():
    return random.choice(ALL)
