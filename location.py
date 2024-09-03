from direction import Direction


class Location:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f'Location({self.x}, {self.y})'

    def __add__(self, other):
        try:
            assert isinstance(other, Direction)
        except AssertionError:
            return self
        new_location = Location(self.x + other.x, self.y + other.y)
        return new_location

    def forward(self, direction):
        return self + direction

    def forward_left(self, direction):
        return self + direction + direction.left()

    def forward_right(self, direction):
        return self + direction + direction.right()

    def distance(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y)

    def step_toward(self, t):
        dx = t.x - self.x
        dy = t.y - self.y
        if abs(dx) > abs(dy):
            step = 1 if dx > 0 else -1
            return Location(self.x + step, self.y)
        else:
            step = 1 if dy > 0 else -1
            return Location(self.x, self.y + step)
