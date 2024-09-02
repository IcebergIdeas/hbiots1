from block import Block
from bot import Bot
from direction import Direction
from map import Map
from world import World


class TestBot:
    def test_step(self):
        world = World(10, 10)
        bot = Bot(5, 5)
        world.add(bot)
        location = bot.location
        bot.direction = Direction.NORTH
        bot.step()
        assert bot.location == location + Direction.NORTH

    def test_bot_facing_north_block(self):
        bot = Bot(5, 5)
        bot.direction = Direction.NORTH
        map = Map(10, 10)
        map.place(bot)
        bot.vision = map.create_vision(bot.location)
        assert not bot.facing_block()
        map.place(Block(5,4))
        bot.vision = map.create_vision(bot.location)
        assert bot.facing_block()

    def test_bot_facing_east_block(self):
        bot = Bot(5, 5)
        bot.direction = Direction.EAST
        map = Map(10, 10)
        map.place(bot)
        bot.vision = map.create_vision(bot.location)
        assert not bot.facing_block()
        map.place(Block(6,5))
        bot.vision = map.create_vision(bot.location)
        assert bot.facing_block()
