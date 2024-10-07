from direct_connection import DirectConnection
from direction import Direction
from location import Location
from world import World


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
        world.add_block(6, 5)
        assert not world.is_empty(Location(6, 5))
        connection.take(client_bot)
        world_bot = world.map.at_id(bot_id)
        assert world_bot.has_block()
        assert world.is_empty(Location(6, 5))

    def test_drop_block_on_open_cell(self):
        world = World(10, 10)
        client_bot = world.add_bot(5, 5)
        bot_id = client_bot.id
        world_bot = world.map.at_id(bot_id)
        client_block = world.add_block(1,9)
        world_block = world.map.at_id(client_block.id)
        world_bot.receive(world_block)
        connection = DirectConnection(world)
        assert len(world.map.contents.keys()) == 2
        connection.drop(client_bot, client_block)
        assert len(world.map.contents.keys()) == 2
        assert not world_bot.has(client_block)
        assert not world.is_empty(Location(6, 5))

    def test_connection_add_bot(self):
        world = World(10, 10)
        connection = DirectConnection(world)
        bot = connection.add_bot(5, 5)
        assert bot.location == Location(5, 5)
