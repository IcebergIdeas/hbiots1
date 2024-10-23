from server.map import Map
from server.world import World
from server.world_entity import WorldEntity
from shared.direct_connection import DirectConnection
from shared.location import Location


class TestScent:
    def test_hookup(self):
        assert 2 + 2 == 4

    def test_empty_map(self):
        map = Map(10, 10)
        scent = map.scent_at(Location(5, 5), 0)
        assert scent == 0

    def test_relative_scent_right_here(self):
        map = Map(10, 10)
        loc = Location (5, 5)
        block = WorldEntity.block(loc.x, loc.y, 0)
        map.place(block)
        scent = map.relative_scent(loc, loc, 0)
        assert scent == 4

    def test_scent_right_here(self):
        map = Map(10, 10)
        loc = Location (5, 5)
        block = WorldEntity.block(loc.x, loc.y, 1)
        map.place(block)
        scent = map.scent_at(loc, 1)
        assert scent == 4

    def test_scent_all_around(self):
        map = Map(10, 10)
        for x in range(11):
            for y in range(11):
                block = WorldEntity.block(x, y, 2)
                map.place(block)
        scent = map.scent_at(Location(5, 5), 2)
        assert scent ==  40

    def test_bots_dont_smell(self):
        world = World(10, 10)
        world.add_bot(5, 5)
        bot_entity = world.map.at_xy(5, 5)
        bot_entity.aroma = 5
        map = world.map
        scent = map.scent_at(Location(5, 5), 5)
        assert scent ==  0

    def test_we_get_scent(self):
        world = World(10, 10)
        world.add_block(5, 5)  # comment?
        client_bot = DirectConnection(world).add_bot(4, 6)
        client_bot.direction_change_chance = 0.0
        client_bot.do_something(DirectConnection(world))
        assert client_bot._knowledge._scent == 3
