from block import Block
from bot import Bot
from direction import Direction
from machine import Machine


class TestMethodObjectStateMachine:
    def test_starts_walking(self):
        bot = Bot(5, 5)
        machine = Machine(bot)
        assert machine._state == machine.walking

    def test_laden_goes_to_walking_if_no_block_in_inventory(self):
        bot = Bot(5, 5)
        machine = Machine(bot)
        machine._state = machine.laden
        machine.state()
        assert machine._state == machine.walking

    def test_looking_goes_to_laden_if_block_in_inventory(self):
        bot = Bot(5, 5)
        machine = Machine(bot)
        vision_list = [('R', 5, 5)]
        bot.vision = vision_list
        machine._state = machine.looking
        machine.state()
        assert machine._state == machine.looking
        bot.receive(Block(2, 2))
        machine.state()
        assert machine._state == machine.laden

    def test_laden_stays_laden_if_cannot_drop(self):
        # we call state() twice to ensure round trip update
        bot = Bot(5, 5)
        machine = Machine(bot)
        entity = Block(3, 3)
        bot.receive(entity)
        vision_list = [('R', 5, 5), ('B', 6, 5)]
        bot.vision = vision_list
        bot.direction = Direction.EAST
        machine._state = machine.laden
        machine.state()
        assert bot.has_block()
        assert machine._state == machine.laden
        machine.state()
        assert bot.has_block()
        assert machine._state == machine.laden