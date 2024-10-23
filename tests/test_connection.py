from server.world import World
from server.world_entity import WorldEntity
from shared.direct_connection import DirectConnection
from shared.direction import Direction
from shared.location import Location


class TestConnection:
    def test_exists(self):
        world = World(20, 20)
        connection = DirectConnection(world)

    def test_step(self):
        world = World(20, 20)
        connection = DirectConnection(world)
        bot = connection.add_bot(10, 10)
        connection.step(bot)
        assert bot.location == Location(11, 10)
        assert world.map.at_xy(11, 10).id == bot.id

    def test_step_north(self):
        world = World(10, 10)
        connection = DirectConnection(world)
        client_bot = connection.add_bot(5, 5, Direction.NORTH)
        location = client_bot.location
        connection.step(client_bot)
        assert client_bot.location == location + Direction.NORTH

    def test_take_a_block(self):
        world = World(10, 10)
        connection = DirectConnection(world)
        client_bot = connection.add_bot(5, 5)
        bot_id = client_bot.id
        world.add_block(6, 5)
        assert not world.is_empty(Location(6, 5))
        connection.take(client_bot)
        world_bot = world.map.at_id(bot_id)
        assert world_bot.has_block()
        assert world.is_empty(Location(6, 5))

    def test_connection_add_bot(self):
        world = World(10, 10)
        connection = DirectConnection(world)
        bot = connection.add_bot(5, 5)
        assert bot.location == Location(5, 5)

    def test_connection_does_not_hold_world_entity(self):
        world = World(10, 10)
        bot_id = world.add_bot(5, 5)
        world_bot = world.map.at_id(bot_id)
        world.add_block(6, 5)
        world.take_forward(world_bot)
        assert world_bot.holding
        info = world.fetch(bot_id)
        assert not isinstance(info['held_entity'], WorldEntity)
