import random

from direction import Direction
from knowledge import Knowledge
from location import Location
from machine import Walking


class Bot:
    def __init__(self, x, y, direction=Direction.EAST):
        self.name = 'R'
        self.direction_change_chance = 0.2
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
    def holding(self):
        return self._knowledge.holding

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

    def has(self, entity):
        return self._knowledge.has(entity)

    def receive(self, entity_id: int):
        self._knowledge.receive(entity_id)

    def remove(self, entity):
        self._knowledge.remove(entity)

    def do_something(self, connection):
        actions = []
        actions += self.update_for_state_machine()
        self.state = self.state.update(self._knowledge)
        actions += self.state.action(self._knowledge)
        if random.random() < self.direction_change_chance:
            actions += self.change_direction()
        actions += ['step']
        self.perform_actions(actions, connection)

    def perform_actions(self, actions, connection):
        for action in actions:
            match action:
                case 'take':
                    connection.take(self)
                case 'drop':
                    connection.drop(self, self.holding)
                case 'step':
                    self._old_location = self.location
                    connection.step(self)
                case 'NORTH' | 'EAST' | 'SOUTH' | 'WEST':
                    connection.set_direction(self, action)
                case _:
                    assert 0, f'no case {action}'

    def update_for_state_machine(self):
        if self.location == self._old_location:
            return self.change_direction()
        else:
            return []

    def has_block(self):
        return self._knowledge.has_block

    def has_no_block(self):
        return not self.has_block()

    def can_take(self):
        return self._knowledge.can_take

    def can_drop(self):
        return self.vision.match_forward_and_one_side('_', 'B')

    def change_direction(self):
        return [self._knowledge.new_direction().name()]

    def forward_location(self):
        return self.location + self.direction
