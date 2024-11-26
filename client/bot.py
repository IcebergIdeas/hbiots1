import random

from client.cohort import Cohort
from client.forwarder import Forwarder
from client.knowledge import Knowledge
from client.machine import Walking
from shared.direction import Direction
from shared.location import Location


class Bot:
    direction = Forwarder('_knowledge')
    holding = Forwarder('_knowledge')
    id = Forwarder('_knowledge')
    location = Forwarder('_knowledge')
    vision = Forwarder('_knowledge')

    def __init__(self, x, y, direction=Direction.EAST):
        self.name = 'R'
        self.direction_change_chance = 0.2
        self._knowledge = Knowledge(Location(x, y), direction)
        self.state = Walking()
        self._old_location = None

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
            connection.run_request(cohort, rq)

    def update(self, result_dict):
        self._knowledge.update(result_dict)

    def has_block(self):
        return self._knowledge.has_block

    def change_direction(self):
        return [self._knowledge.new_direction().name()]
