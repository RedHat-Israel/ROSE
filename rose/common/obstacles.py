""" Game obstacles """

import random

NONE    = ""
CRACK   = "crack"
TRASH   = "trash"
PENGUIN = "penguin"
BIKE    = "bike"
WATER   = "water"
BARRIER = "barrier"

ALL = (NONE, CRACK, TRASH, PENGUIN, BIKE, WATER, BARRIER)


def get_random_obstacle():
    return random.choice(ALL)
