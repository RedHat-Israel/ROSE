"""
Random driver

This is a rather silly driver choosing the next action randomly. It is not a
very good driver but the implementation is very elegant.
"""
import random
from rtp.common import obstacles, actions


def drive(your_car_location, world):
    return random.choice(actions.ALL)
