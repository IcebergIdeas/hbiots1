from block import Block
from direction import Direction
from location import Location
from vision import Vision


class Knowledge:
    def __init__(self):
        self._old_location = None
        self._location = None
        self._direction = None
        self._vision = Vision([], None, None)
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

    @property
    def has_block(self):
        return self._entity



class TestDecisions:
    def test_initial_knowledge(self):
        knowledge = Knowledge()
        knowledge.location = Location(10, 10)
        assert knowledge.has_moved

    def test_move(self):
        knowledge = Knowledge()
        knowledge.location = Location(10, 10)
        knowledge.location = Location(10, 9)
        assert knowledge.has_moved

    def test_no_move(self):
        knowledge = Knowledge()
        knowledge.location = Location(10, 10)
        knowledge.location = Location(10, 10)
        assert not knowledge.has_moved

    def test_can_take(self):
        knowledge = Knowledge()
        knowledge.location = Location(10, 10)
        knowledge.direction = Direction.NORTH
        vision_list = [('B', 10, 9)]
        knowledge.vision = vision_list
        assert knowledge.can_take

    def test_can_drop(self):
        knowledge = Knowledge()
        knowledge.location = Location(10, 10)
        knowledge.direction = Direction.NORTH
        vision_list = [('B', 10, 9)]
        knowledge.vision = vision_list
        assert not knowledge.can_drop
        knowledge.vision = [('B', 9, 9)]
        assert knowledge.can_drop
        knowledge.vision = [('B', 11, 9)]
        assert knowledge.can_drop


    def test_has_block(self):
        knowledge = Knowledge()
        assert not knowledge.has_block
        block = Block(3, 3)
        knowledge.receive(block)
        assert knowledge.has_block
        knowledge.remove(block)
        assert not knowledge.has_block
