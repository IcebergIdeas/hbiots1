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
        map = Map(10, 10)
        bot = Bot(5, 5)
        bot.direction = Direction.NORTH
        map.place(bot)
        bot.vision = map.vision_at(bot.location)
        assert not bot.can_take()
        map.place(Block(5,4))
        bot.vision = map.vision_at(bot.location)
        assert bot.can_take()

    def test_bot_facing_east_block(self):
        map = Map(10, 10)
        bot = Bot(5, 5)
        bot.direction = Direction.EAST
        map.place(bot)
        bot.vision = map.vision_at(bot.location)
        assert not bot.can_take()
        map.place(Block(6,5))
        bot.vision = map.vision_at(bot.location)
        assert bot.can_take()
