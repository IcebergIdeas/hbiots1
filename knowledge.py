from vision import Vision


class Knowledge:
    def __init__(self, location, direction):
        self._old_location = None
        self._location = location
        self._direction = direction
        self._vision = Vision([], self.location, self.direction)
        self._entity = None

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
        return entity == self._entity

    @property
    def has_block(self):
        return self._entity and self._entity.name == 'B'

    @property
    def has_moved(self):
        return self.location != self._old_location

    @property
    def can_take(self):
        return self.vision.match_forward_and_one_side('B', '_')

    @property
    def can_drop(self):
        return self.vision.match_forward_and_one_side('_', 'B')

    def receive(self, entity):
        self._entity = entity

    def remove(self, entity):
        if self._entity == entity:
            self._entity = None

