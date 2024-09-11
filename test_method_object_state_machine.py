from block import Block
from bot import Bot
from direction import Direction
from machine import Machine


class TestMethodObjectStateMachine:
    def test_starts_walking(self):
        bot = Bot(5, 5)
        machine = Machine(bot._knowledge)
        assert machine._action == machine.walking_action

    def test_laden_goes_to_walking_if_no_block_in_inventory(self):
        bot = Bot(5, 5)
        machine = Machine(bot._knowledge)
        machine.set_states(machine.laden_states())
        machine.state(bot._knowledge)
        assert machine._action == machine.walking_action

    def test_looking_goes_to_walking_then_laden_if_block_in_inventory(self):
        bot = Bot(5, 5)
        vision_list = [('R', 5, 5)]
        bot.vision = vision_list
        machine = Machine(bot._knowledge)
        machine.set_states(machine.looking_states())
        assert not machine._knowledge.has_block
        machine.state(bot._knowledge)
        assert machine._action == machine.looking_action
        bot.receive(Block(2, 2))
        assert machine._knowledge.has_block
        machine.state(bot._knowledge)
        assert machine._action == machine.walking_action
        machine.tired = 0
        machine.state(bot._knowledge)
        assert machine._action == machine.laden_action

    def test_laden_stays_laden_if_cannot_drop(self):
        # we call state() twice to ensure round trip update
        bot = Bot(5, 5)
        entity = Block(3, 3)
        bot.receive(entity)
        vision_list = [('R', 5, 5), ('B', 6, 5)]
        bot.vision = vision_list
        machine = Machine(bot._knowledge)
        bot.direction = Direction.EAST
        machine.set_states(machine.laden_states())
        machine.state(bot._knowledge)
        assert bot.has_block()
        assert machine._action == machine.laden_action
        machine.state(bot._knowledge)
        assert bot.has_block()
        assert machine._action == machine.laden_action

    def test_laden_goes_walkabout_after_drop(self):
        bot = Bot(5, 5)
        machine = Machine(bot._knowledge)
        entity = Block(3, 3)
        bot.receive(entity)
        vision_list = [('R', 5, 5), ('B', 6, 6)]
        bot.vision = vision_list
        bot.direction = Direction.EAST
        machine.tired = 0
        machine.set_states(machine.laden_states())
        assert bot.has_block()
        assert machine._action == machine.laden_action
        actions = machine.state(bot._knowledge)
        assert 'drop' in actions
        machine._knowledge.remove(machine._knowledge._entity)
        _ = machine.state(bot._knowledge)
        assert machine._action == machine.walking_action

    def test_unladen_goes_from_walking_to_looking(self):
        bot = Bot(5, 5)
        machine = Machine(bot._knowledge)
        assert machine.tired == 10
        assert machine._action == machine.walking_action
        machine.state(bot._knowledge)
        assert machine.tired == 9
        assert machine._action == machine.walking_action
        machine.tired = 0
        machine.state(bot._knowledge)
        assert machine._action == machine.looking_action


