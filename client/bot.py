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
        actions = self.get_intended_actions()
        self.record_expectations(actions)
        return actions

    def get_intended_actions(self):
        actions = []
        actions += self.check_expectations()
        actions += self.updated_state_action()
        actions += self.possibly_change_direction()
        actions += ['step']
        return actions

    def updated_state_action(self):
        self.state = self.state.update(self._knowledge)
        return self.state.action(self._knowledge)

    def possibly_change_direction(self):
        if random.random() < self.direction_change_chance:
            return self.change_direction()
        else:
            return []

    def record_expectations(self, actions):
        if 'step' in actions:
            self._old_location = self.location

    def check_expectations(self):
        if self.location == self._old_location:
            return self.change_direction()
        else:
            return []

    def perform_actions_only_for_tests(self, actions, connection):
        cohort = Cohort(self)
        for action in actions:
            match action:
                case 'drop':
                    rq = [ { 'entity': self.id, 'verb': 'drop', 'holding': self.holding}]
                case 'step' | 'take' | 'NORTH' | 'EAST' | 'SOUTH' | 'WEST' as verb:
                    rq = [ {'entity': self.id, 'verb': verb} ]
                case _:
                    assert 0, f'no case {action}'
            connection.run_request(cohort, None, rq)

    def update(self, result_dict):
        self._knowledge.update(result_dict)

    def has_block(self):
        return self._knowledge.has_block

    def can_take(self):
        return self._knowledge.can_take

    def can_drop(self):
        return self.vision.match_forward_and_one_side('_', 'B')

    def change_direction(self):
        return [self._knowledge.new_direction().name()]

    def forward_location(self):
        return self.location + self.direction
