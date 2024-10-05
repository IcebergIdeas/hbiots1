
class WorldEntity:
    def __init__(self):
        self._dict = dict()

    @property
    def id(self):
        return self._dict['id']

    @id.setter
    def id(self, value):
        self._dict['id'] = value


class TestWorldEntity:
    def is_valid(self, entity):
        try:
            assert entity._dict['id'] == entity.id
            return True
        except KeyError:
            return False

    def test_create(self):
        WorldEntity()

    def test_set_and_fetch(self):
        entity = WorldEntity()
        entity.id = 102
        assert entity.id == 102
        assert self.is_valid(entity)