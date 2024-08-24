from enum import Enum

class Direction:
    NORTH = None
    EAST = None
    SOUTH = None
    WEST = None
    ALL = None

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
        return Direction(new_x, new_y)


Direction.NORTH = Direction(0, -1)
Direction.EAST = Direction(1, 0)
Direction.SOUTH = Direction(0, 1)
Direction.WEST = Direction(-1, 0)
Direction.ALL = [Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST]
