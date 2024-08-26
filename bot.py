import random

from direction import Direction
from point import Point


class Bot:
    def __init__(self, x, y, direction=Direction.EAST):
        self.world = None
        self.id = None
        self.name = 'R'
        self.location = Point(x, y)
        self.direction = direction
        self.direction_change_chance = 0.2
        self.inventory = []
        self.tired = 10
        self.state = "walking"

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

    def is_close_enough(self, entity):
        return entity.location.distance(self.location) < 10

    def do_something(self):
        if self.state == "walking":
            self.move()
            self.tired -= 1
            if self.tired <= 0:
                self.state = "looking"
        elif self.state == "looking":
            if self.beside_block():
                self.take()
                self.state = "laden"
                self.tired = 5
        elif self.state == "laden":
            if self.tired <= 0:
                self.world.drop(self, self.inventory[0])
                self.inventory = []
                self.tired = 5
                self.state = "walking"

    def beside_block(self):
        return True

    def take(self):
        self.world.take(self)

    def move(self):
        old_location = self.location
        if random.random() < self.direction_change_chance:
            self.change_direction()
        self.step()
        if self.location == old_location:
            self.change_direction()

    def step(self):
        self.world.step(self, self.direction)

    def change_direction(self):
        direction = self.direction
        while direction == self.direction:
            direction = random.choice(Direction.ALL)
        self.direction = direction

    def move_north(self):
        self.world.move(self, Direction.NORTH)

    def move_east(self):
        self.world.move(self, Direction.EAST)

    def move_south(self):
        self.world.move(self, Direction.SOUTH)

    def move_west(self):
        self.world.move(self, Direction.WEST)

    def drop_south(self):
        self.world.drop_south(self)

    def drop_west(self):
        self.world.drop_west(self)
