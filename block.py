from point import Point


class Block:
    def __init__(self, x, y):
        self.world = None
        self.id = None
        self.name = 'B'
        self.location = Point(x, y)

    @property
    def x(self):
        return self.location.x

    @property
    def y(self):
        return self.location.y

    def is_close_enough(self, entity):
        pe = entity.location
        se = self.location
        d = pe.distance(se)
        return d < 3
