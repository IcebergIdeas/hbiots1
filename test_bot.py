import pytest

from block import Block
from bot import Bot
from direct_connection import DirectConnection
from direction import Direction
from knowledge import Knowledge
from location import Location
from machine import Looking
from world import World
from world_entity import WorldEntity


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

    def test_take_a_block(self):
        world = World(10, 10)
        client_bot = DirectConnection(world).add_bot(5, 5)
        world.add_block(6, 5)
        assert not world.is_empty(Location(6, 5))
        world.take_forward(client_bot)
        assert client_bot.has_block()
        assert world.is_empty(Location(6, 5))

    def test_bot_facing_north_takes_a_north_block(self):
        world = World(10, 10)
        bot = DirectConnection(world).add_bot(5, 5)
        world.add_block(5, 4)
        bot.direction = Direction.NORTH
        world.take_forward(bot)
        assert bot.has_block()

    def test_bot_facing_east_takes_an_east_block(self):
        world = World(10, 10)
        bot = DirectConnection(world).add_bot(5, 5)
        world.add_block(6, 5)
        world.take_forward(bot)
        assert bot.has_block()

    def test_bot_facing_south_takes_a_south_block(self):
        world = World(10, 10)
        bot = DirectConnection(world).add_bot(5, 5)
        world.add_block(5, 6)
        bot.direction = Direction.SOUTH
        world.take_forward(bot)
        assert bot.has_block()

    def test_bot_facing_west_takes_a_west_block(self):
        world = World(10, 10)
        bot = DirectConnection(world).add_bot(5, 5)
        world.add_block(4, 5)
        bot.direction = Direction.WEST
        world.take_forward(bot)
        assert bot.has_block()

    def test_bot_cant_take_diagonally(self):
        world = World(10, 10)
        bot = DirectConnection(world).add_bot(5, 5)
        world.add_block(4, 4)
        world.add_block(6, 4)
        world.add_block(4, 6)
        world.add_block(6, 6)
        world.take_forward(bot)
        assert not bot.has_block()

    def test_bot_cannot_drop_off_world_north(self):
        world = World(10, 10)
        bot = DirectConnection(world).add_bot(5, 0)
        block = Block(4, 4)
        bot.receive(block)
        bot.direction = Direction.NORTH
        world.drop_forward(bot, block)
        assert bot.has(block), 'drop should not happen'

    def test_bot_cannot_drop_off_world_east(self):
        world = World(10, 10)
        bot = DirectConnection(world).add_bot(10, 5)
        block = Block(4, 4)
        bot.receive(block)
        bot.direction = Direction.EAST
        world.drop_forward(bot, block)
        assert bot.has(block), 'drop should not happen'

    def test_bot_cannot_drop_off_world_south(self):
        world = World(10, 10)
        bot = DirectConnection(world).add_bot(5, 10)
        block = Block(4, 4)
        bot.receive(block)
        bot.direction = Direction.SOUTH
        world.drop_forward(bot, block)
        assert bot.has(block), 'drop should not happen'

    def test_bot_cannot_drop_off_world_west(self):
        world = World(10, 10)
        bot = DirectConnection(world).add_bot(0, 5)
        block = Block(4, 4)
        bot.receive(block)
        bot.direction = Direction.WEST
        world.drop_forward(bot, block)
        assert bot.has(block), 'drop should not happen'
