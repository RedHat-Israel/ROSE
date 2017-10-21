import logging
import random
import os
from rose.common import config
import component

log = logging.getLogger('car')

class Car(component.Component):

    def __init__(self, id, x, y):
        self.id = id
        self.x = None
        self.y = None
        self.texture = None
        self.name = None

    def update(self, info):
        self.x = info['x']
        self.y = info['y']
        self.name = info['name']
