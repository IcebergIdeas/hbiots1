from point import Point


class Biot:
    def __init__(self):
        self.location = Point(0, 0)

    def update(self, info):
        self.location = info["location"]
