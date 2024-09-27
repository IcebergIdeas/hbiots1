import random

from direction import Direction
from knowledge import Knowledge
from location import Location
from machine import Walking


class Bot:
    def __init__(self, x, y, direction=Direction.EAST):
        self.world = None
        self.name = 'R'
        self.direction_change_chance = 0.2
        self.tired = 10
        self._knowledge = Knowledge(Location(x, y), direction)
        self.state = Walking()
        self._old_location = None

    @property
    def id(self):
        return self._knowledge.id

    @id.setter
    def id(self, id):
        self._knowledge.id = id

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
    def scent(self):
        return self._knowledge._scent

    @scent.setter
    def scent(self, scent):
        self._knowledge._scent = scent

    @property
    def x(self):
        return self.location.x

    @property
    def y(self):
        return self.location.y

    def has(self, entity):
        return self._knowledge.has(entity)

    def receive(self, entity):
        self._knowledge.receive(entity)

    def remove(self, entity):
        self._knowledge.remove(entity)

    def do_something(self):
        self.update_knowledge()
        self.state = self.state.update(self._knowledge)
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

    def update_knowledge(self):
        self._knowledge.gain_energy()
        if self.location == self._old_location:
            self.change_direction()

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

    def move(self):
        if random.random() < self.direction_change_chance:
            self.change_direction()
        self._old_location = self.location
        self.step()

    def step(self):
        self.world.step(self)
        self.tired -= 1

    def change_direction(self):
        direction = self.direction
        while direction == self.direction:
            direction = random.choice(Direction.ALL)
        self.direction = direction
