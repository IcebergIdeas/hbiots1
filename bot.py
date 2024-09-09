import random

from direction import Direction
from location import Location
from machine import Machine
from vision import Vision


class Bot:
    def __init__(self, x, y, direction=Direction.EAST):
        self.world = None
        self.id = None
        self.name = 'R'
        self.location = Location(x, y)
        self.direction = direction
        self.direction_change_chance = 0.2
        self.inventory = []
        self._vision = None
        self.tired = 10
        self.state = Machine(self)

    @property
    def vision(self):
        return self._vision

    @vision.setter
    def vision(self, vision):
        self._vision = Vision(vision, self.location, self.direction)

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
        self.update()
        self.state.state()
        self.move()

    def update(self):
        pass

    def has_block(self):
        return self.has_inventory('B')

    def has_no_block(self):
        return not self.has_block()

    def has_inventory(self, entity_name):
        for entity in self.inventory:
            if entity.name == entity_name:
                return True
        return False

    def can_take(self):
        return self.vision.forward_name() == 'B' and (self.vision.forward_left_name() == '_' or self.vision.forward_right_name() == '_')

    def can_drop(self):
        return self.vision.forward_name() == '_' and (self.vision.forward_left_name() == 'B' or self.vision.forward_right_name() == 'B')

    def take(self):
        self.world.take_forward(self)

    def drop(self, entity):
        self.world.drop_forward(self, entity)

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
