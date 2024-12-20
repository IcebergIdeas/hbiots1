
class Direction:
    NORTH = None
    EAST = None
    SOUTH = None
    WEST = None
    ALL = None
    EVERY = None
    ALL_NAMES = ['NORTH', 'EAST', 'SOUTH', 'WEST']

    def __init__(self, x, y):
        self.x = x
        self.y = y

        if Direction.NORTH is None:
            Direction.NORTH = True # avoid recursion forever
            Direction.NORTH = Direction(0, -1)
            Direction.EAST = Direction(1, 0)
            Direction.SOUTH = Direction(0, 1)
            Direction.WEST = Direction(-1, 0)
            Direction.CENTER = Direction(0, 0)
            Direction.NORTH_WEST = Direction(-1, -1)
            Direction.NORTH_EAST = Direction(1, -1)
            Direction.SOUTH_WEST = Direction(-1, 1)
            Direction.SOUTH_EAST = Direction(1, 1)
            Direction.ALL = (Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST)
            Direction.EVERY = (Direction.NORTH_WEST, Direction.NORTH, Direction.NORTH_EAST,
                               Direction.WEST, Direction.CENTER, Direction.EAST,
                               Direction.SOUTH_WEST, Direction.SOUTH, Direction.SOUTH_EAST)

    @classmethod
    def from_name(cls, string):
        match string:
            case 'NORTH':
                return cls.NORTH
            case 'EAST':
                return cls.EAST
            case 'SOUTH':
                return cls.SOUTH
            case 'WEST':
                return cls.WEST
            case _:
                return cls.EAST

    def __add__(self, other):
        if isinstance(other, Direction):
            return Direction(self.x + other.x, self.y + other.y)
        else:
            return other + self

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f'Direction({self.x}, {self.y})'

    def left(self):
        x, y = self.x, self.y
        new_x, new_y = y, -x
        return Direction(new_x, new_y)

    def right(self):
        x, y = self.x, self.y
        new_x, new_y = -y, x
        return Direction(new_x, new_y)

    def name(self):
        match self:
            case Direction.NORTH:
                return 'NORTH'
            case Direction.EAST:
                return 'EAST'
            case Direction.SOUTH:
                return 'SOUTH'
            case Direction.WEST:
                return 'WEST'
            case _:
                raise ValueError

init = Direction(0,1)