import random

from direction import Direction
from point import Point


class Bot:
    def __init__(self, x, y):
        self.world = None
        self.id = None
        self.name = 'R'
        self.location = Point(x, y)
        self.direction = Direction.EAST
        self.direction_change_chance = 0.2
        self.inventory = []

    @property
    def x(self):
        return self.location.x

    @property
    def y(self):
        return self.location.y

    def scan(self):
        return self.world.scan(self)

    def has(self, entity):
        return entity in self.inventory

    def receive(self, entity):
        self.inventory.append(entity)

    def pick_up_block(self):
        result = self.scan()
        if self.block_to_east(result):
            self.take_east()

    def take_east(self):
        self.world.take_east(self)
    #
    # def take(self, direction):
    #     self.world.take(self,  direction)

    def block_to_east(self, result):
        return True

    def is_close_enough(self, entity):
        return entity.location.distance(self.location) < 10

    def do_something(self):
        self.pick_up_block()
        old_location = self.location
        if random.random() < self.direction_change_chance:
            self.change_direction()
        self.step_in_direction()
        if self.location == old_location:
            self.change_direction()

    def step_in_direction(self):
        d = self.direction
        if d == Direction.NORTH:
            self.world.move_north(self)
        elif d == Direction.EAST:
            self.world.move_east(self)
        elif d == Direction.SOUTH:
            self.world.move_south(self)
        elif d == Direction.WEST:
            self.world.move_west(self)

    def change_direction(self):
        direction = self.direction
        while direction == self.direction:
            direction = random.choice(list(Direction))
        self.direction = direction

    def move_north(self):
        self.world.move_north(self)

    def move_east(self):
        self.world.move_east(self)

    def move_south(self):
        self.world.move_south(self)

    def move_west(self):
        self.world.move_west(self)

    def drop_south(self):
        self.world.drop_south(self)

    def drop_west(self):
        self.world.drop_west(self)
