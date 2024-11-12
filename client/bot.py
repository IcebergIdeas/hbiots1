import random

from client.cohort import Cohort
from client.knowledge import Knowledge
from client.machine import Walking
from shared.direction import Direction
from shared.location import Location


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

    def do_something_only_for_tests(self, connection):
        actions = self.get_actions()
        self.perform_actions_only_for_tests(actions, connection)
        return actions

    def get_actions(self):
        actions = []
        actions += self.turn_if_we_didnt_move()
        self.state = self.state.update(self._knowledge)
        actions += self.state.action(self._knowledge)
        if random.random() < self.direction_change_chance:
            actions += self.change_direction()
        actions += ['step']
        return actions

    def perform_actions_only_for_tests(self, actions, connection):
        cohort = Cohort(self)
        for action in actions:
            match action:
                case 'take':
                    connection.take(cohort, self.id)
                case 'drop':
                    # self.holding is an id
                    connection.drop(cohort, self.id, self.holding)
                case 'step':
                    self._old_location = self.location
                    connection.step(cohort, self.id)
                case 'NORTH' | 'EAST' | 'SOUTH' | 'WEST':
                    connection.turn(cohort, self.id, action)
                case _:
                    assert 0, f'no case {action}'

    def update(self, result_dict):
        self._knowledge.update(result_dict)

    def turn_if_we_didnt_move(self):
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
