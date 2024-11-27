from random import choice

from client.vision import Vision
from shared.direction import Direction


class Knowledge:
    drop_threshold = 4
    take_threshold = 7
    energy_threshold = 5

    def __init__(self, location, direction):
        # world write / client read only
        self.direction = direction
        self.id = None
        self.location = location
        self._held_entity = None
        self._scent = 0
        self._vision = Vision([], self.location, self.direction)
        # local Bot client-side info
        self._energy = self.energy_threshold

    def update(self, update_dictionary):
        self.direction = update_dictionary['direction']
        self.id = update_dictionary['eid']
        self.location = update_dictionary['location']
        self.receive(update_dictionary['held_entity'])
        self._scent = update_dictionary['scent']
        self.vision = update_dictionary['vision']

    @property
    def vision(self) -> Vision:
        return self._vision

    @vision.setter
    def vision(self, vision_list):
        self._vision = Vision(vision_list, self.location, self.direction)

    @property
    def holding(self):
        return self._held_entity

    @property
    def has_block(self):
        return self._held_entity  # and self._held_entity.name == 'B'

    @property
    def can_take(self):
        is_scent_ok = self._scent <= self.take_threshold
        return is_scent_ok and self.vision.match_forward_and_one_side('B', '_')

    @property
    def can_drop(self):
        vision_ok = self.vision.match_forward_and_one_side('_', 'B')
        scent_ok = self._scent >= self.drop_threshold
        return vision_ok and scent_ok

    def has(self, entity):
        return entity == self._held_entity

    def has_energy(self):
        return self._energy >= self.energy_threshold

    def new_direction(self):
        possibles = [d for d in Direction.ALL if d != self.direction]
        return choice(possibles)

    def new_direction_name(self):
        return self.new_direction().name()

    def use_energy(self):
        self._energy = 0

    def gain_energy(self):
        self._energy += 1

    def receive(self, entity):
        self._held_entity = entity

    def remove(self, entity):
        if self._held_entity == entity:
            self._held_entity = None
