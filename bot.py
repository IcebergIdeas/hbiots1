import random

from direction import Direction
from location import Location
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
        self.state = self.walking

    @property
    def vision(self):
        return self._vision

    @vision.setter
    def vision(self, vision):
        self._vision = Vision(vision)

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
        self.state()
        self.move()

    def walking(self):
        if self.tired <= 0:
            self.state = self.looking

    def looking(self):
        if self.facing_block():
            self.take()
            if self.inventory:
                self.tired = 5
                self.state = self.laden

    def laden(self):
        if self.tired <= 0:
            if self.near_block():
                block = self.inventory[0]
                self.world.drop_forward(self, block)
                if block not in self.inventory:
                    self.tired = 5
                    self.state = self.walking

    def facing_block(self):
        return self.forward_name() == 'B' and (self.forward_left_name() == '_' or self.forward_right_name() == '_')

    def forward_name(self):
        forward = self.location.forward(self.direction)
        return self.vision.name_at(forward)

    def forward_left_name(self):
        forward_left = self.location.forward_left(self.direction)
        return self.vision.name_at(forward_left)

    def forward_right_name(self):
        forward_right = self.location.forward_right(self.direction)
        return self.vision.name_at(forward_right)

    def near_block(self):
        return self.forward_name() == '_' and (self.forward_left_name() == 'B' or self.forward_right_name() == 'B')

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
