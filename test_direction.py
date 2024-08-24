class NewDirection:
    NORTH = None
    EAST = None
    SOUTH = None
    WEST = None

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f'({self.x}, {self.y})'

    def left(self):
        x, y = self.x, self.y
        new_x, new_y = y, -x
        return NewDirection(new_x, new_y)


NewDirection.NORTH = NewDirection(0, -1)
NewDirection.EAST = NewDirection(1, 0)
NewDirection.SOUTH = NewDirection(0, 1)
NewDirection.WEST = NewDirection(-1, 0)

class TestDirection:
    def test_hookup(self):
        assert 2 + 2 == 4

    def test_direction_EAST(self):
        dir = NewDirection.EAST

    def test_direction_left(self):
        east = NewDirection.EAST
        assert east.left() == NewDirection.NORTH

