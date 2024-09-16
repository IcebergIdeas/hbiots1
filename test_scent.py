from block import Block
from bot import Bot
from location import Location
from map import Map
from world import World


class TestScent:
    def test_hookup(self):
        assert 2 + 2 == 4

    def test_empty_map(self):
        map = Map(10, 10)
        scent = map.scent_at(Location(5, 5))
        assert scent == 0

    def test_relative_scent_right_here(self):
        map = Map(10, 10)
        loc = Location (5, 5)
        block = Block(loc.x, loc.y)
        map.place(block)
        scent = map.relative_scent(loc, loc)
        assert scent == 4

    def test_scent_right_here(self):
        map = Map(10, 10)
        loc = Location (5, 5)
        block = Block(loc.x, loc.y)
        map.place(block)
        scent = map.scent_at(loc)
        assert scent == 4

    def test_scent_all_around(self):
        map = Map(10, 10)
        for x in range(11):
            for y in range(11):
                block = Block(x, y)
                block.id = 11*x + y
                map.place(block)
        scent = map.scent_at(Location (5, 5))
        assert scent ==  40

    def test_bots_dont_smell(self):
        map = Map(10, 10)
        for x in range(11):
            for y in range(11):
                block = Bot(x, y)
                block.id = 11*x + y
                map.place(block)
        scent = map.scent_at(Location (5, 5))
        assert scent ==  0

    def test_we_get_scent(self):
        world = World(10, 10)
        block = Block(5, 5)
        world.add(block)
        bot = Bot(4, 6)
        world.add(bot)
        world.step(bot)
        assert bot._knowledge.scent == 3
