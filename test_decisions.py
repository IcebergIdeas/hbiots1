from block import Block
from bot import Bot
from direction import Direction
from knowledge import Knowledge
from location import Location


class TestDecisions:
    def test_initial_knowledge(self):
        knowledge = Knowledge()
        knowledge.location = Location(10, 10)
        assert knowledge.has_moved

    def test_move(self):
        knowledge = Knowledge()
        knowledge.location = Location(10, 10)
        knowledge.location = Location(10, 9)
        assert knowledge.has_moved

    def test_no_move(self):
        knowledge = Knowledge()
        knowledge.location = Location(10, 10)
        knowledge.location = Location(10, 10)
        assert not knowledge.has_moved

    def test_can_take(self):
        knowledge = Knowledge()
        knowledge.location = Location(10, 10)
        knowledge.direction = Direction.NORTH
        vision_list = [('B', 10, 9)]
        knowledge.vision = vision_list
        assert knowledge.can_take

    def test_can_drop(self):
        knowledge = Knowledge()
        knowledge.location = Location(10, 10)
        knowledge.direction = Direction.NORTH
        vision_list = [('B', 10, 9)]
        knowledge.vision = vision_list
        assert not knowledge.can_drop
        knowledge.vision = [('B', 9, 9)]
        assert knowledge.can_drop
        knowledge.vision = [('B', 11, 9)]
        assert knowledge.can_drop

    def test_has_block(self):
        knowledge = Knowledge()
        assert not knowledge.has_block
        block = Block(3, 3)
        knowledge.receive(block)
        assert knowledge.has_block
        knowledge.remove(block)
        assert not knowledge.has_block

    def test_bot_uses_knowledge_inventory(self):
        bot = Bot(5, 5)
        block = Block(3, 3)
        bot.receive(block)
        assert bot._knowledge.has_block
