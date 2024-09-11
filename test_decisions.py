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

    def receive(self, entity):
        self._entity = entity

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

    def test_vision(self):
        knowledge = Knowledge()
        knowledge.location = Location(10, 10)
        knowledge.direction = Direction.NORTH
        vision_list = [('B', 10, 9)]
        knowledge.vision = vision_list
        assert knowledge.can_take

    def test_has_block(self):
        knowledge = Knowledge()
        assert not knowledge.has_block
        block = Block(3, 3)
        knowledge.receive(block)
        assert knowledge.has_block
