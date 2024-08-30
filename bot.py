import random

from direction import Direction
from point import Point

"""
B_.
_R_
...
"""

class Bot:
    def __init__(self, x, y, direction=Direction.EAST):
        self.world = None
        self.id = None
        self.name = 'R'
        self.location = Point(x, y)
        self.direction = direction
        self.direction_change_chance = 0.2
        self.inventory = []
        self._vision = None
        self.tired = 10
        self.state = "walking"

    @property
    def vision(self):
        return self._vision

    @vision.setter
    def vision(self, vision):
        self._vision = vision

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

    def remove(self, entity):
        try:
            self.inventory.remove(entity)
        except ValueError:
            pass

    def is_close_enough(self, entity):
        return entity.location.distance(self.location) < 10

    def do_something(self):
        if self.state == "walking":
            if self.tired <= 0:
                self.state = "looking"
        elif self.state == "looking":
            if self.beside_block():
                self.take()
                if self.inventory:
                    self.tired = 5
                    self.state = "laden"
        elif self.state == "laden":
            if self.tired <= 0:
                if self.beside_block():
                    block = self.inventory[0]
                    self.world.drop_forward(self, block)
                    if block not in self.inventory:
                        self.tired = 5
                        self.state = "walking"
        self.move()

    def beside_block(self):
        return True

    def take(self):
        self.world.take_forward(self)

    def move(self):
        if random.random() < self.direction_change_chance:
            self.change_direction()
        step_succeeded = self.took_a_step()
        if not step_succeeded:
            self.change_direction()

    def took_a_step(self):
        old_location = self.location
        self.step()
        return self.location != old_location

    def step(self):
        self.world.step(self)
        self.tired -= 1

    def change_direction(self):
        direction = self.direction
        while direction == self.direction:
            direction = random.choice(Direction.ALL)
        self.direction = direction


