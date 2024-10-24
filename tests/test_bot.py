import pytest

from client.bot import Bot
from client.knowledge import Knowledge
from client.machine import Looking
from server.world import World
from server.world_entity import WorldEntity
from shared.direct_connection import DirectConnection
from shared.direction import Direction
from shared.location import Location


class TestBot:
    # Seems to have redundant tests, needs cleanup

    def test_create_bot(self):
        bot = Bot(10, 10)
        assert isinstance(bot, Bot)

    def test_starting_location(self):
        bot = Bot(10, 10)
        assert bot.location == Location(10, 10)

    def test_bot_in_world_gets_next_id(self):
        WorldEntity.next_id = 100
        world = World(10, 10)
        bot = DirectConnection(world).add_bot(5, 5)
        assert bot.id == 101

    def test_wandering(self):
        world = World(10, 10)
        connection = DirectConnection(world)
        client_bot = connection.add_bot(5, 5)
        client_bot.do_something(connection)
        loc = client_bot.location
        assert loc != Location(5, 5)

    def test_change_direction_if_stuck(self):
        world = World(10, 10)
        connection = DirectConnection(world)
        client_bot = connection.add_bot(9, 5)
        client_bot.direction_change_chance = 0.0
        client_bot.do_something(connection)
        assert client_bot.location == Location(10, 5)
        assert client_bot.direction == Direction.EAST
        client_bot.do_something(connection)
        assert client_bot.location == Location(10, 5)
        client_bot.do_something(connection)
        assert client_bot.location != Location(10, 5)
        world_bot = world.map.at_id(client_bot.id)
        assert world_bot.direction != Direction.EAST
        assert client_bot.direction != Direction.EAST

    def test_requests_direction_change_if_stuck(self):
        bot = Bot(10, 10)
        bot._old_location = Location(10, 10)
        actions = bot.update_for_state_machine()
        assert actions[0] in ["NORTH", "SOUTH", "WEST"]

    def test_stop_at_edge(self):
        world = World(10, 10)
        connection = DirectConnection(world)
        client_bot = connection.add_bot(9, 5)
        client_bot.direction_change_chance = 0
        client_bot.do_something(connection)
        assert client_bot.location == Location(10, 5)
        client_bot.do_something(connection)
        assert client_bot.location == Location(10, 5)
        client_bot.do_something(connection)
        assert client_bot.location != Location(10, 5)

# Some of these are redundant, moved from another file
    @pytest.mark.skip("too weird")
    def test_bot_notices_a_block(self):
        world = World(10, 10)
        client_bot = DirectConnection(world).add_bot(5, 5)
        client_bot.state._energy = Knowledge.energy_threshold
        client_bot.direction_change_chance = 0
        real_bot = world.map.at_id(client_bot.id)
        real_bot.direction_change_chance = 0
        real_bot.state._energy = Knowledge.energy_threshold
        block = world.add_block(7, 5)
        world.set_bot_vision(client_bot)
        world.set_bot_vision(real_bot)
        world.set_bot_scent(client_bot)
        world.set_bot_scent(real_bot)
        client_bot.do_something(DirectConnection(world))
        world.update_client_for_test(client_bot)
        assert isinstance(client_bot.state, Looking)
        client_bot.do_something(DirectConnection(world))
        world.update_client_for_test(client_bot)
        assert client_bot.has(block)

    def test_bot_cant_take_diagonally(self):
        world = World(10, 10)
        bot = DirectConnection(world).add_bot(5, 5)
        world.add_block(4, 4)
        world.add_block(6, 4)
        world.add_block(4, 6)
        world.add_block(6, 6)
        world.take_forward(bot)
        assert not bot.has_block()

    def test_bot_drops_and_world_receives(self):
        world = World(10, 10)
        connection = DirectConnection(world)
        client_bot = connection.add_bot(5, 5)
        world.add_block(6, 5)
        block = world.map.at_xy(6, 5)
        assert isinstance(block, WorldEntity)
        connection.take(client_bot)
        assert client_bot.has_block()
        assert not world.map.at_xy(6, 5)
        connection.drop(client_bot, client_bot.holding)
        test_block = world.map.at_xy(6, 5)
        assert isinstance(test_block, WorldEntity)
