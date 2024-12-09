from server.map import Map
from server.map_test_entity import MapTestEntity
from server.world_entity import WorldEntity
from shared.direction import Direction
from shared.location import Location


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
        block = WorldEntity.block(3, 4)
        world_map.place(block)
        other_map = FakeMap()
        map_entry = MapTestEntity(3, 4, 'B')
        other_map.contents.append(map_entry)
        assert world_map.map_is_OK(other_map)

    def test_map_successful_move(self):
        map = Map(10, 10)
        bot = WorldEntity.bot(5, 5, Direction.EAST)
        map.place(bot)
        map.attempt_move(bot.key, Location(6, 6))
        assert bot.location == Location(6, 6)

    def test_map_unsuccessful_move(self):
        map = Map(10, 10)
        bot = WorldEntity.bot(5, 5, Direction.EAST)
        map.place(bot)
        map.attempt_move(bot.key, Location(10, 11))
        assert bot.location == Location(5, 5)

    def test_map_recognizes_open_location(self):
        map = Map(10, 10)
        location = Location(5, 5)
        assert map.location_is_open((location))
        block = WorldEntity.block(5, 5)
        map.place(block)
        assert not map.location_is_open(location)

    def test_map_off_world_not_open(self):
        map = Map(10,10)
        for x,y in ((-1, 5), (5, -1), (11, 5), (5, 11)):
            location = Location(x, y)
            assert not map.location_is_open(location)
