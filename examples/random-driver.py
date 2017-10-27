"""
Random driver

This is a rather silly driver choosing the next action randomly. It is not a
very good driver but the implementation is very elegant.
"""
import random
from rose.common import obstacles, actions  # NOQA

attribute = [
    "Furious",
    "Big",
    "Rolling"
]

names = [
    "Mike",
    "Sally",
    "Jackson",
    "Sam",
    "Jane",
    "Bruce"
]

server_address = "localhost"
driver_name = "{0} {1}".format(random.choice(attribute), random.choice(names))


def drive(world):
    return random.choice(actions.ALL)
