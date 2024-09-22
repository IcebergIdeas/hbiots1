from location import Location


class Block:
    def __init__(self, x, y):
        self.world = None
        self.id = None
        self.name = 'B'
        self.location = Location(x, y)

    @property
    def x(self):
        return self.location.x

    @property
    def y(self):
        return self.location.y

    def __str__(self):
        return f'{self.name} {str(self.location)}'
