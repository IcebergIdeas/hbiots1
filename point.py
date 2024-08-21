class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f'Point({self.x}, {self.y})'

    def distance(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y)

    def step_toward(self, t):
        dx = t.x - self.x
        dy = t.y - self.y
        if abs(dx) > abs(dy):
            step = 1 if dx > 0 else -1
            return Point(self.x + step, self.y)
        else:
            step = 1 if dy > 0 else -1
            return Point(self.x, self.y + step)
