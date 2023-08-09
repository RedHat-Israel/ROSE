""" Game obstacles """

import random

NONE    = ""         # NOQA
CRACK   = "crack"    # NOQA
TRASH   = "trash"    # NOQA
PENGUIN = "penguin"  # NOQA
BIKE    = "bike"     # NOQA
WATER   = "water"    # NOQA
BARRIER = "barrier"  # NOQA
BOOSTER = "booster"

ALL = (NONE, CRACK, TRASH, PENGUIN, BIKE, WATER, BARRIER, BOOSTER)


def get_random_obstacle():
    return random.choice(ALL)
