from . import component


class Car(component.Component):
    def __init__(self, id):
        self.id = id
        self.x = None
        self.y = None
        self.name = None

    def update(self, info):
        self.x = info["x"]
        self.y = info["y"]
        self.name = info["name"]
