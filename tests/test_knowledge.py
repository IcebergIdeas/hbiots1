from client.bot import Bot
from client.knowledge import Knowledge
from server.world_entity import WorldEntity
from shared.direction import Direction
from shared.location import Location


class TestKnowledge:
    def test_knowledge_take_decision(self):
        location = Location(10, 10)
        direction = Direction.NORTH
        knowledge = Knowledge(location, direction)
        knowledge.vision = [('B', 10, 9)]
        knowledge._scent = Knowledge.take_threshold
        assert knowledge.can_take

    def test_knowledge_take_decision_high_scent(self):
        location = Location(10, 10)
        direction = Direction.NORTH
        knowledge = Knowledge(location, direction)
        knowledge.vision = [('B', 10, 9)]
        knowledge._scent = Knowledge.take_threshold + 1
        assert not knowledge.can_take

    def test_can_drop(self):
        location = Location(10, 10)
        direction = Direction.NORTH
        knowledge = Knowledge(location, direction)
        knowledge.vision = [('B', 10, 9)]
        knowledge._scent = Knowledge.drop_threshold
        assert not knowledge.can_drop
        knowledge.vision = [('B', 9, 9)]
        assert knowledge.can_drop
        knowledge.vision = [('B', 11, 9)]
        assert knowledge.can_drop

    def test_has_block(self):
        knowledge = Knowledge(None, None)
        assert not knowledge.has_block
        block = WorldEntity.block(3, 3)
        knowledge.receive(block)
        assert knowledge.has_block
        knowledge.remove(block)
        assert not knowledge.has_block

    def test_bot_uses_knowledge_inventory(self):
        bot = Bot(5, 5)
        block = WorldEntity.block(3, 3)
        bot.receive(block)
        assert bot._knowledge.has_block

    def test_knowledge_drop_decision(self):
        location = Location(5, 5)
        direction = Direction.NORTH
        knowledge = Knowledge(location, direction)
        vision_list = [('R', 5, 5), ('B', 4, 4)]
        knowledge.vision = vision_list
        knowledge._scent = Knowledge.drop_threshold
        assert knowledge.can_drop

    def test_knowledge_drop_decision_low_scent(self):
        location = Location(5, 5)
        direction = Direction.NORTH
        knowledge = Knowledge(location, direction)
        vision_list = [('R', 5, 5), ('B', 4, 4)]
        knowledge.vision = vision_list
        knowledge._scent = Knowledge.drop_threshold - 1
        assert not knowledge.can_drop

    def test_knowledge_drop_decision_other_side(self):
        location = Location(5, 5)
        direction = Direction.NORTH
        knowledge = Knowledge(location, direction)
        vision_list = [('R', 5, 5), ('B', 6, 4)]
        knowledge.vision = vision_list
        knowledge._scent = Knowledge.drop_threshold
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


