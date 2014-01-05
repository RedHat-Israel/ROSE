import random
from components import matrix_config


def drive():
    return random.choice(matrix_config.ACTIONS)
