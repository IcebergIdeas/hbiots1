from entities import Entities


class FakeMap:
    def get_entities(self):
        return []


class TestMapping:
    def test_hookup(self):
        assert 4 == 2 + 2

    def test_map_compare(self):
        map = Entities()
        other_map = FakeMap()
        assert map == other_map
