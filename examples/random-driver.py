"""
Random driver

This is a rather silly driver choosing the next action randomly. It is not a
very good driver but the implementation is very elegant.
"""
import random
from rose.common import obstacles, actions  # NOQA

driver_name = "Random Driver"


def drive(world):
    return random.choice(actions.ALL)
