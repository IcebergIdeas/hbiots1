
class Direction:
    NORTH = None
    EAST = None
    SOUTH = None
    WEST = None
    ALL = None
    EVERY = None

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        if isinstance(other, Direction):
            return Direction(self.x + other.x, self.y + other.y)
        else:
            return other + self

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f'({self.x}, {self.y})'

    def left(self):
        x, y = self.x, self.y
        new_x, new_y = y, -x
        return Direction(new_x, new_y)

    def right(self):
        return self.left().left().left()


Direction.NORTH = Direction(0, -1)
Direction.EAST = Direction(1, 0)
Direction.SOUTH = Direction(0, 1)
Direction.WEST = Direction(-1, 0)
Direction.CENTER = Direction(0, 0)
Direction.NORTH_WEST = Direction(-1, -1)
Direction.NORTH_EAST = Direction(1, -1)
Direction.SOUTH_WEST = Direction(-1, 1)
Direction.SOUTH_EAST = Direction(1, 1)
Direction.ALL = [Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST]
Direction.EVERY = [Direction.NORTH_WEST, Direction.NORTH, Direction.NORTH_EAST,
                   Direction.WEST, Direction.CENTER, Direction.EAST,
                   Direction.SOUTH_WEST, Direction.SOUTH, Direction.SOUTH_EAST]
