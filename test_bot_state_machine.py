from block import Block
from bot import Bot
from direction import Direction


class TestBotStateMachine:
    def test_laden_goes_to_walking_if_no_block_in_inventory(self):
        bot = Bot(5, 5)
        bot.tired = 0
        bot.state = bot.laden
        bot.state()
        assert bot.state == bot.walking

    def test_looking_goes_to_laden_if_block_in_inventory(self):
        bot = Bot(5, 5)
        bot.tired = 0
        vision_list = [('R', 5, 5)]
        bot.vision = vision_list
        bot.state = bot.looking
        bot.state()
        assert bot.state == bot.looking
        bot.receive(Block(2, 2))
        bot.state()
        assert bot.state == bot.laden

    def test_laden_stays_laden_if_cannot_drop(self):
        # we call state() twice to ensure round trip update
        bot = Bot(5, 5)
        bot.tired = 0
        entity = Block(3, 3)
        bot.receive(entity)
        vision_list = [('R', 5, 5), ('B', 6, 5)]
        bot.vision = vision_list
        bot.direction = Direction.EAST
        bot.state = bot.laden
        bot.state()
        assert bot.has_block()
        assert bot.state == bot.laden
        bot.state()
        assert bot.has_block()
        assert bot.state == bot.laden


