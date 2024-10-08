from bot import Bot
from direct_connection import DirectConnection
from location import Location
from map import Map
from world import World
from world_entity import WorldEntity


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
        block = WorldEntity.block(loc.x, loc.y)
        map.place(block)
        scent = map.relative_scent(loc, loc, 0)
        assert scent == 4

    def test_scent_right_here(self):
        map = Map(10, 10)
        loc = Location (5, 5)
        block = WorldEntity.block(loc.x, loc.y)
        map.place(block)
        scent = map.scent_at(loc, 0)
        assert scent == 4

    def test_scent_all_around(self):
        map = Map(10, 10)
        for x in range(11):
            for y in range(11):
                block = WorldEntity.block(x, y)
                map.place(block)
        scent = map.scent_at(Location(5, 5), 0)
        assert scent ==  40

    def test_bots_dont_smell(self):
        map = Map(10, 10)
        for x in range(11):
            for y in range(11):
                block = Bot(x, y)
                block.id = 11*x + y
                map.place(block)
        scent = map.scent_at(Location(5, 5), 0)
        assert scent ==  0

    def test_we_get_scent(self):
        world = World(10, 10)
        world.add_block(5, 5)  # comment?
        client_bot = world.add_bot(4, 6)
        client_bot.direction_change_chance = 0.0
        client_bot.do_something(DirectConnection(world))
        assert client_bot._knowledge._scent == 3
