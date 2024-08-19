from block import Block
from entities import Entities


class FakeMap:
    def __init__(self):
        self.contents = list()

    def get_entities(self):
        return []


class TestMapping:
    def test_hookup(self):
        assert 4 == 2 + 2

    def test_map_compare(self):
        map = Entities()
        other_map = FakeMap()
        assert map == other_map

    def test_map_with_block(self):
        world_map = Entities()
        block = Block(3, 4)
        world_map.place(block)
        other_map = FakeMap()
        other_map.contents.append({'x': 3, 'y': 4, 'name': 'B'})
