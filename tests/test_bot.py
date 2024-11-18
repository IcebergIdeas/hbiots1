import json

import pytest

from client.bot import Bot
from client.cohort import Cohort
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
        client_bot.do_something_only_for_tests(connection)
        loc = client_bot.location
        assert loc != Location(5, 5)

    def test_change_direction_if_stuck(self):
        world = World(10, 10)
        connection = DirectConnection(world)
        client_bot = connection.add_bot(9, 5)
        client_bot.direction_change_chance = 0.0
        client_bot.do_something_only_for_tests(connection)
        assert client_bot.location == Location(10, 5)
        assert client_bot.direction == Direction.EAST
        client_bot.do_something_only_for_tests(connection)
        assert client_bot.location == Location(10, 5)
        client_bot.do_something_only_for_tests(connection)
        assert client_bot.location != Location(10, 5)
        world_bot = world.map.at_id(client_bot.id)
        assert world_bot.direction != Direction.EAST
        assert client_bot.direction != Direction.EAST

    def test_requests_direction_change_if_stuck(self):
        bot = Bot(10, 10)
        bot._old_location = Location(10, 10)
        actions = bot.check_expectations()
        assert actions[0] in ["NORTH", "SOUTH", "WEST"]

    def test_stop_at_edge(self):
        world = World(10, 10)
        connection = DirectConnection(world)
        client_bot = connection.add_bot(9, 5)
        client_bot.direction_change_chance = 0
        actions = client_bot.do_something_only_for_tests(connection)
        assert actions == ['step']
        assert client_bot.location == Location(10, 5)
        actions = client_bot.do_something_only_for_tests(connection)
        assert actions == ['step']
        assert client_bot.location == Location(10, 5)
        actions = client_bot.do_something_only_for_tests(connection)
        assert actions[0] in ["NORTH", "SOUTH", "EAST", "WEST"]
        assert actions[1] == 'step'
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
        client_bot.do_something_only_for_tests(DirectConnection(world))
        world.update_client_for_test(client_bot)
        assert isinstance(client_bot.state, Looking)
        client_bot.do_something_only_for_tests(DirectConnection(world))
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
        cohort = Cohort(client_bot)

        block_id = world.add_block(6, 5)
        assert (block := world.map.at_xy(6, 5)) is not None

        self.do_take(cohort, connection, client_bot)
        assert client_bot.has_block()
        assert world.map.at_xy(6, 5) is None

        self.do_drop(cohort, connection, client_bot, block_id)
        assert world.map.at_xy(6, 5) is block

    def do_drop(self, cohort, connection, client_bot, block_id):
        rq = [{'entity': client_bot.id, 'verb': 'drop', 'holding': block_id}]
        connection.run_request(cohort, rq)

    def do_take(self, cohort, connection, client_bot):
        rq1 = [{'entity': client_bot.id, 'verb': 'take'}]
        connection.run_request(cohort, rq1)

    def test_bot_sets_old_location(self):
        bot = Bot(10, 10)
        assert bot._old_location is None
        actions = bot.get_actions()
        assert 'step' in actions
        assert bot._old_location == Location(10, 10)

    def test_cannot_set_into_knowledge(self):
        bot = Bot(10, 10)
        with pytest.raises(KeyError):
            bot.id = 101

    def test_json(self):
        s = json.dumps('3')
        assert s == '"3"'
        s = json.dumps([1, 2, 3])
        assert s == '[1, 2, 3]'
        t = json.loads(s)
        assert t == [1, 2, 3]
        d = { 'a': {
            'x': "hello",
            'y': 37
        }}
        s = json.dumps(d)
        assert s == '{"a": {"x": "hello", "y": 37}}'
