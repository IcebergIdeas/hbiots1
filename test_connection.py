import copy

from block import Block
from direction import Direction
from location import Location
from world import World


class DirectConnection:
    def __init__(self, world):
        self.world = world

    def step(self, bot):
        self.world.command('step', bot.id)
        result = self.world.fetch(bot.id)
        bot._knowledge = copy.copy(result)

    def take(self, client_bot):
        self.world.command('take', client_bot.id)
        result = self.world.fetch(client_bot.id)
        client_bot._knowledge = copy.copy(result)

    def drop(self, client_bot, block):
        self.world.command('drop', client_bot.id, block.id)
        result = self.world.fetch(client_bot.id)
        client_bot._knowledge = copy.copy(result)


class TestConnection:
    def test_exists(self):
        world = World(20, 20)
        connection = DirectConnection(world)

    def test_step(self):
        world = World(20, 20)
        bot = world.add_bot(10, 10)
        connection = DirectConnection(world)
        connection.step(bot)
        assert bot.location == Location(11, 10)
        assert world.map.at_xy(11, 10).id == bot.id

    def test_step_north(self):
        world = World(10, 10)
        client_bot = world.add_bot(5, 5, Direction.NORTH)
        location = client_bot.location
        connection = DirectConnection(world)
        connection.step(client_bot)
        assert client_bot.location == location + Direction.NORTH

    def test_take_a_block(self):
        world = World(10, 10)
        client_bot = world.add_bot(5, 5)
        bot_id = client_bot.id
        connection = DirectConnection(world)
        block = Block(6, 5)
        world.add(block)
        assert not world.is_empty(Location(6, 5))
        connection.take(client_bot)
        world_bot = world.map.at_id(bot_id)
        assert world_bot.has(block)
        assert world.is_empty(Location(6, 5))

    def test_drop_block_on_open_cell(self):
        world = World(10, 10)
        client_bot = world.add_bot(5, 5)
        bot_id = client_bot.id
        world_bot = world.map.at_id(bot_id)
        block = Block(1, 9)
        world.add(block)
        world_bot.receive(block)
        connection = DirectConnection(world)
        assert len(world.map.contents.keys()) == 2
        connection.drop(client_bot, block)
        assert len(world.map.contents.keys()) == 2
        assert not world_bot.has(block)
        assert not world.is_empty(Location(6, 5))
