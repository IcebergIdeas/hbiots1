from block import Block
from bot import Bot
from location import Location
from map import Map
from map_entry import MapEntity


class FakeMap:
    def __init__(self):
        self.contents = list()

    def get_entities(self):
        return self.contents


class TestMap:
    def test_hookup(self):
        assert 4 == 2 + 2

    def test_map_compare(self):
        world_map = Map(10, 10)
        other_map = FakeMap()
        assert world_map.map_is_OK(other_map)

    def test_map_with_block(self):
        world_map = Map(10, 10)
        block = Block(3, 4)
        world_map.place(block)
        other_map = FakeMap()
        map_entry = MapEntity(3, 4, 'B')
        other_map.contents.append(map_entry)
        assert world_map.map_is_OK(other_map)

    def test_map_successful_move(self):
        map = Map(10, 10)
        bot = Bot(5,5)
        map.place(bot)
        map.attempt_move(bot.id, Location(6,6))
        assert bot.location == Location(6,6)

    def test_map_unsuccessful_move(self):
        map = Map(10, 10)
        bot = Bot(5,5)
        map.place(bot)
        map.attempt_move(bot.id, Location(10, 11))
        assert bot.location == Location(5, 5)

