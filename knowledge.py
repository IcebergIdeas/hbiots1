from vision import Vision


class Knowledge:
    drop_threshold = 4
    take_threshold = 7
    energy_threshold = 5

    def __init__(self, location, direction):
        # world write / client read only
        self._direction = direction
        self._held_entity = None
        self._id = None
        self._location = location
        self._scent = 0
        self._vision = Vision([], self.location, self.direction)
        # local Bot client-side info
        self._energy = self.energy_threshold
        self._old_location = None

    @property
    def holding(self):
        return self._held_entity

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        self._id = id

    def has_energy(self):
        return self._energy >= self.energy_threshold

    def use_energy(self):
        self._energy = 0

    def gain_energy(self):
        self._energy += 1

    @property
    def vision(self) -> Vision:
        return self._vision

    @vision.setter
    def vision(self, vision_list):
        self._vision = Vision(vision_list, self.location, self.direction)

    @property
    def direction(self):
        return self._direction

    @direction.setter
    def direction(self, direction):
        self._direction = direction

    @property
    def location(self):
        return self._location

    @location.setter
    def location(self, location):
        self._old_location = self.location
        self._location = location

    def has(self, entity):
        return entity == self._held_entity

    @property
    def has_block(self):
        return self._held_entity and self._held_entity.name == 'B'

    @property
    def has_moved(self):
        return self.location != self._old_location

    @property
    def can_take(self):
        is_scent_ok = self._scent <= self.take_threshold
        return is_scent_ok and self.vision.match_forward_and_one_side('B', '_')

    @property
    def can_drop(self):
        is_scent_ok = self._scent >= self.drop_threshold
        return is_scent_ok and self.vision.match_forward_and_one_side('_', 'B')

    def receive(self, entity):
        self._held_entity = entity

    def remove(self, entity):
        if self._held_entity == entity:
            self._held_entity = None

