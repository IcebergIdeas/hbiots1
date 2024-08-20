from point import Point


class Bot:
    def __init__(self, x, y):
        self.world = None
        self.id = None
        self.name = 'R'
        self.location = Point(x, y)

    @property
    def x(self):
        return self.location.x

    @property
    def y(self):
        return self.location.y

    def scan(self):
        return self.world.scan(self)

    def is_close_enough(self, entity):
        pe = entity.location
        se = self.location
        d = pe.distance(se)
        return d < 3
