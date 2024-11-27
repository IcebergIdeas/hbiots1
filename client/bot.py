import random

from client.forwarder import Forwarder
from client.knowledge import Knowledge
from client.machine import Walking
from shared.direction import Direction
from shared.location import Location


class Bot:
    holding = Forwarder('_knowledge')
    id = Forwarder('_knowledge')
    location = Forwarder('_knowledge')
    new_direction_name = Forwarder('_knowledge')
    update = Forwarder('_knowledge')

    def __init__(self, x, y, direction=Direction.EAST):
        self.name = 'R'
        self.direction_change_chance = 0.2
        self._knowledge = Knowledge(Location(x, y), direction)
        self.state = Walking()
        self._old_location = None

    def change_direction(self):
        return [self.new_direction_name()]

    def check_expectations(self):
        if self.location == self._old_location:
            return self.change_direction()
        else:
            return []

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

    def possibly_change_direction(self):
        if random.random() < self.direction_change_chance:
            return self.change_direction()
        else:
            return []

    def record_expectations(self, actions):
        if 'step' in actions:
            self._old_location = self.location

    def updated_state_action(self):
        self.state = self.state.update(self._knowledge)
        return self.state.action(self._knowledge)
