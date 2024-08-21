import random

from point import Point


class Bot:
    def __init__(self, x, y):
        self.world = None
        self.id = None
        self.name = 'R'
        self.location = Point(x, y)
        self.direction = 'east'

    @property
    def x(self):
        return self.location.x

    @property
    def y(self):
        return self.location.y

    def scan(self):
        return self.world.scan(self)

    def is_close_enough(self, entity):
        return entity.location.distance(self.location) < 10

    def do_something(self):
        old_location = self.location
        self.step_in_direction()
        if self.location == old_location:
            self.change_direction()
            self.step_in_direction()

    def step_in_direction(self):
        d = self.direction
        if d == 'east':
            self.world.move_east(self)
        elif d == 'north':
            self.world.move_north(self)
        elif d == 'south':
            self.world.move_south(self)
        elif d == 'west':
            self.world.move_west(self)

    def change_direction(self):
        self.direction = random.choice(['north', 'south', 'east', 'west'])

