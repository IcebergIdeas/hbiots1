from point import Point


class Biot:
    def __init__(self):
        self.id = None
        self.location = Point(0, 0)

    def update(self, info):
        self.id = info["ID"]
        self.location = info["location"]
