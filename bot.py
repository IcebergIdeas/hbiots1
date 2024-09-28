import random

from direct_connection import DirectConnection
from direction import Direction
from knowledge import Knowledge
from location import Location
from machine import Walking


class Bot:
    def __init__(self, x, y, direction=Direction.EAST):
        self.world = None
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
        actions = []
        actions += self.update_for_state_machine()
        self.state = self.state.update(self._knowledge)
        actions += self.state.action(self._knowledge)
        if random.random() < self.direction_change_chance:
            actions += self.change_direction()
        self._old_location = self.location
        actions += ['step']
        self.perform_actions(actions)

    def perform_actions(self, actions):
        connection = DirectConnection(self.world)
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
        self._knowledge.gain_energy()
        if self.location == self._old_location:
            new_direction = self.change_direction()
            return new_direction
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

    def move(self):
        if random.random() < self.direction_change_chance:
            self.change_direction()
        self._old_location = self.location
        self.step()

    def step(self):
        self.perform_actions(['step'])

    def change_direction(self):
        direction = self.direction
        while direction == self.direction:
            direction = random.choice(Direction.ALL)
        return [direction.name()]
