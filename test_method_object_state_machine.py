from block import Block
from bot import Bot
from direction import Direction
from machine import Machine


class TestMethodObjectStateMachine:
    def test_starts_walking(self):
        bot = Bot(5, 5)
        machine = Machine(bot)
        assert machine._action == machine.walking

    def test_laden_goes_to_walking_if_no_block_in_inventory(self):
        bot = Bot(5, 5)
        machine = Machine(bot)
        machine._update = machine.update_laden
        machine._action = machine.laden
        machine.state(bot)
        assert machine._action == machine.walking

    def test_looking_goes_to_walking_then_laden_if_block_in_inventory(self):
        bot = Bot(5, 5)
        vision_list = [('R', 5, 5)]
        bot.vision = vision_list
        machine = Machine(bot)
        machine._update = machine.update_looking
        machine._action = machine.looking
        machine.state(bot)
        assert machine._action == machine.looking
        bot.receive(Block(2, 2))
        machine.state(bot)
        assert machine._action == machine.walking
        machine.tired = 0
        machine.state(bot)
        assert machine._action == machine.laden

    def test_laden_stays_laden_if_cannot_drop(self):
        # we call state() twice to ensure round trip update
        bot = Bot(5, 5)
        entity = Block(3, 3)
        bot.receive(entity)
        vision_list = [('R', 5, 5), ('B', 6, 5)]
        bot.vision = vision_list
        machine = Machine(bot)
        bot.direction = Direction.EAST
        machine._action = machine.laden
        machine.state(bot)
        assert bot.has_block()
        assert machine._action == machine.laden
        machine.state(bot)
        assert bot.has_block()
        assert machine._action == machine.laden

    def test_laden_goes_walkabout_after_drop(self):
        bot = Bot(5, 5)
        machine = Machine(bot)
        entity = Block(3, 3)
        bot.receive(entity)
        vision_list = [('R', 5, 5)]
        bot.vision = vision_list
        bot.direction = Direction.EAST
        machine._update = machine.update_laden
        machine._action = machine.laden
        machine.state(bot)
        assert bot.has_block()
        assert machine._action == machine.laden
        bot.remove(entity)
        machine.state(bot)
        assert not bot.has_block()
        assert machine._action == machine.walking

    def test_unladen_goes_from_walking_to_looking(self):
        bot = Bot(5, 5)
        machine = Machine(bot)
        assert machine.tired == 10
        assert machine._action == machine.walking
        machine.state(bot)
        assert machine.tired == 9
        assert machine._action == machine.walking
        machine.tired = 0
        machine.state(bot)
        assert machine._action == machine.looking
