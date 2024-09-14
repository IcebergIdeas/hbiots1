from block import Block
from bot import Bot
from direction import Direction
from machine import Machine, Looking, Laden, Walking
from world import World


class TestMethodObjectStateMachine:
    def test_starts_walking(self):
        bot = Bot(5, 5)
        machine = Machine(bot._knowledge)
        assert isinstance(machine._state, Walking)

    def test_laden_goes_to_walking_if_no_block_in_inventory(self):
        bot = Bot(5, 5)
        machine = Machine(bot._knowledge)
        machine.set_states((None, None, Laden()))
        machine.state(bot._knowledge)
        assert isinstance(machine._state, Walking)

    def test_looking_goes_to_walking_then_laden_if_block_in_inventory(self):
        bot = Bot(5, 5)
        vision_list = [('R', 5, 5)]
        bot.vision = vision_list
        machine = Machine(bot._knowledge)
        machine.set_states((None, None, Looking()))
        assert not machine._knowledge.has_block
        machine.state(bot._knowledge)
        assert machine._action == None  # looking
        bot.receive(Block(2, 2))
        assert machine._knowledge.has_block
        machine.state(bot._knowledge)
        assert isinstance(machine._state, Walking)
        machine._knowledge.tired = 0
        machine.state(bot._knowledge)
        assert machine._action == None
        assert isinstance(machine._state, Laden)

    def test_laden_stays_laden_if_cannot_drop(self):
        # we call state() twice to ensure round trip update
        bot = Bot(5, 5)
        entity = Block(3, 3)
        bot.receive(entity)
        vision_list = [('R', 5, 5), ('B', 6, 5)]
        bot.vision = vision_list
        machine = Machine(bot._knowledge)
        bot.direction = Direction.EAST
        machine.set_states((None, None, Laden()))
        machine.state(bot._knowledge)
        assert bot.has_block()
        assert isinstance(machine._state, Laden)
        machine.state(bot._knowledge)
        assert bot.has_block()
        assert isinstance(machine._state, Laden)

    def test_laden_goes_walkabout_after_drop(self):
        bot = Bot(5, 5)
        machine = Machine(bot._knowledge)
        entity = Block(3, 3)
        bot.receive(entity)
        vision_list = [('R', 5, 5), ('B', 6, 6)]
        bot.vision = vision_list
        bot.direction = Direction.EAST
        machine.tired = 0
        machine.set_states((None, None, Laden()))
        assert bot.has_block()
        assert isinstance(machine._state, Laden)
        actions = machine.state(bot._knowledge)
        assert 'drop' in actions
        machine._knowledge.remove(machine._knowledge._entity)
        _ = machine.state(bot._knowledge)
        assert isinstance(machine._state, Walking)

    def test_unladen_goes_from_walking_to_looking(self):
        bot = Bot(5, 5)
        machine = Machine(bot._knowledge)
        machine._knowledge.tired = 10
        assert machine._knowledge.tired == 10
        assert isinstance(machine._state, Walking)
        machine.state(bot._knowledge)
        assert machine._knowledge.tired == 9
        assert isinstance(machine._state, Walking)
        machine._knowledge.tired = 0
        machine.state(bot._knowledge)
        assert machine._action is None
        assert isinstance( machine._state, Looking)

    def test_drop(self):
        bot = Bot(5, 5)
        machine = Machine(bot._knowledge)
        his_block = Block(1,1)
        world_block = Block(8, 8)
        world = World(10,10)
        world.add(bot)
        world.add(world_block)
        # vision = world.map.create_vision(Location(7, 7))
        # assert vision == ""
        bot.receive(his_block)
        machine = bot.state
        assert isinstance(machine._state, Walking)
        machine._knowledge.tired = 0
        bot.do_something()
        assert isinstance( machine._state, Laden)
        assert bot._knowledge.has_block



