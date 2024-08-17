from point import Point


class Biot:
    def __init__(self):
        self.id = None
        self.name = 'R'
        self.location = Point(0, 0)


class Block:
    def __init__(self, x, y):
        self.id = None
        self.name = 'B'
        self.location = Point(x, y)
