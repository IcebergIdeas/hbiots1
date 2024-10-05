from direction import Direction
from location import Location


class WorldEntity:
    def __init__(self):
        self._dict = dict()

    @property
    def id(self):
        return self._dict['id']

    @id.setter
    def id(self, value):
        self._dict['id'] = value

    @property
    def direction(self):
        return self._dict['direction']

    @direction.setter
    def direction(self, value):
        self._dict['direction'] = value

    @property
    def location(self):
        return self._dict['location']

    @location.setter
    def location(self, value):
        self._dict['location'] = value

    @property
    def scent(self):
        return self._dict['scent']

    @scent.setter
    def scent(self, value):
        self._dict['scent'] = value

    @property
    def vision(self):
        return self._dict['vision']

    @vision.setter
    def vision(self, value):
        self._dict['vision'] = value



class TestWorldEntity:
    def is_valid(self, entity):
        assert entity._dict['id'] == entity.id
        assert entity._dict['direction'] == entity.direction
        assert entity._dict['location'] == entity.location
        assert entity._dict['scent'] == entity.scent
        assert entity._dict['vision'] == entity.vision
        return True

    def test_create(self):
        WorldEntity()

    def test_set_and_fetch(self):
        entity = WorldEntity()
        entity.id = 102
        assert entity.id == 102
        entity.direction = Direction.EAST
        assert entity.direction == Direction.EAST
        entity.location = Location(6,4)
        assert entity.location == Location(6,4)
        entity.scent = 37
        assert entity.scent == 37
        entity.vision = []
        assert entity.vision == []
        assert self.is_valid(entity)