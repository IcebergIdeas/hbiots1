import random

from direction import Direction
from knowledge import Knowledge
from location import Location
from machine import Walking


class Bot:
    def __init__(self, x, y, direction=Direction.EAST):
        self.world = None
        self.id = None
        self.name = 'R'
        self.direction_change_chance = 0.2
        self.tired = 10
        self._knowledge = Knowledge(Location(x, y), direction)
        self.state = Walking()

    @property
    def direction(self):
        return self._knowledge.direction

    @direction.setter
    def direction(self, direction):
        self._knowledge.direction = direction

    @property
    def inventory(self):
        if self._knowledge._entity:
            return [self._knowledge._entity,]
        else:
            return []

    @property
    def location(self):
        return self._knowledge.location

    @location.setter
    def location(self, location):
        self._knowledge.location = location

    @property
    def vision(self):
        return self._knowledge.vision

    @vision.setter
    def vision(self, vision):
        self._knowledge.vision = vision

    @property
    def x(self):
        return self.location.x

    @property
    def y(self):
        return self.location.y

    def scan(self):
        return self.world.scan(self)

    def has(self, entity):
        return self._knowledge.has(entity)

    def receive(self, entity):
        self._knowledge.receive(entity)

    def remove(self, entity):
        self._knowledge.remove(entity)

    def is_close_enough(self, entity):
        return entity.location.distance(self.location) < 10

    def do_something(self):
        self.update()
        self._knowledge.tired -= 1
        self.state = self.state.update(None, self._knowledge)
        self.do_state_actions()
        self.move()

    def do_state_actions(self):
        for action in self.state.action(self._knowledge):
            match action:
                case 'take':
                    self.world.take_forward(self)
                case 'drop':
                    self.world.drop_forward(self, self.inventory[0])
                case _:
                    assert 0, f'no case {action}'

    def update(self):
        pass

    def has_block(self):
        return self._knowledge.has_block

    def has_no_block(self):
        return not self.has_block()

    def has_inventory(self, entity_name):
        for entity in self.inventory:
            if entity.name == entity_name:
                return True
        return False

    def can_take(self):
        return self._knowledge.can_take

    def can_drop(self):
        return self.vision.match_forward_and_one_side('_', 'B')

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
