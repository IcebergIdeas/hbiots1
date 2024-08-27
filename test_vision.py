import re

from block import Block
from bot import Bot
from direction import Direction
from point import Point
from world import World


class TestVision:
    def test_hookup(self):
        assert True

    def test_nothing_near(self):
        world = World(10, 10)
        bot = Bot(5, 5)
        bot.direction_change_chance = 0.0
        world.add(bot)
        bot.vision = None
        bot.move()
        assert bot.location == Point(6, 5)
        vision = bot.vision
        assert ('R', 6, 5) in vision

    def test_three_blocks_near(self):
        from block import Block
        world = World(10, 10)
        world.add(Block(4, 4))
        world.add(Block(6, 6))
        world.add(Block(4, 5))
        bot = Bot(6, 5)
        bot.direction = Direction.WEST
        bot.direction_change_chance = 0.0
        world.add(bot)
        bot.vision = None
        bot.move()
        assert bot.location == Point(5, 5)
        vision = bot.vision
        assert ('R', 5, 5) in vision
        assert ('B', 4, 5) in vision
        assert ('B', 6, 6) in vision
        assert ('B', 4, 4) in vision

    def test_a_pattern(self):
        vision ='B_B'\
                '_RB'\
                'B__'
        pattern = r'B_..R....'
        result = re.search(pattern, vision)
        assert result
        pattern = r'.B._RBBBB'
        result = re.search(pattern, vision)
        assert not result

