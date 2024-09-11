from location import Location


class Knowledge:
    def __init__(self):
        self._old_location = None
        self._location = None

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
