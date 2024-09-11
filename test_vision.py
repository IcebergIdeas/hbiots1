import re

from bot import Bot
from direction import Direction
from knowledge import Knowledge
from location import Location
from vision import Vision
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
        assert bot.location == Location(6, 5)
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
        assert bot.location == Location(5, 5)
        vision = bot.vision
        assert ('R', 5, 5) in vision
        assert ('B', 4, 5) in vision
        assert ('B', 6, 6) in vision
        assert ('B', 4, 4) in vision

    def test_knowledge_drop_decision(self):
        location = Location(5, 5)
        direction = Direction.NORTH
        knowledge = Knowledge(location, direction)
        vision_list = [('R', 5, 5), ('B', 4, 4)]
        knowledge.vision = vision_list
        assert knowledge.can_drop

    def test_knowledge_drop_decision_other_side(self):
        location = Location(5, 5)
        direction = Direction.NORTH
        knowledge = Knowledge(location, direction)
        vision_list = [('R', 5, 5), ('B', 6, 4)]
        knowledge.vision = vision_list
        assert knowledge.can_drop

    def test_knowledge_cant_drop_none_around(self):
        location = Location(5, 5)
        direction = Direction.WEST
        knowledge = Knowledge(location, direction)
        vision_list = [('R', 5, 5)]
        knowledge.vision = vision_list
        assert not knowledge.can_drop

    def test_knowledge_cant_drop_block_in_front(self):
        location = Location(5, 5)
        direction = Direction.EAST
        knowledge = Knowledge(location, direction)
        vision_list = [('R', 5, 5), ('B', 6, 5)]
        knowledge.vision = vision_list
        assert not knowledge.can_drop
