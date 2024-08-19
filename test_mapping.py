from block import Block
from entities import Entities


class FakeMap:
    def __init__(self):
        self.contents = list()

    def get_entities(self):
        return self.contents


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
        map_entry = {'x': 3, 'y': 4, 'name': 'B'}
        other_map.contents.append(map_entry)
        assert world_map == other_map
        # assert world.map_is_OK(other_map)
