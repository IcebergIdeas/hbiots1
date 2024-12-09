import json

import pytest

from client.bot import Bot
from client.cohort import Cohort
from server.world import World
from server.world_entity import WorldEntity
from shared.direct_connection import DirectConnection
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

    def test_wandering_better(self):
        bot = Bot(5, 5)
        actions = bot.get_actions()
        assert 'step' in actions

    def test_requests_direction_change_if_stuck(self):
        bot = Bot(10, 10)
        bot._old_location = Location(10, 10)
        actions = bot.check_expectations()
        assert actions[0] in ["NORTH", "SOUTH", "WEST"]

# Some of these are redundant, moved from another file
    def test_bot_cant_take_diagonally(self):
        world = World(10, 10)
        client_bot = DirectConnection(world).add_bot(5, 5)
        world_bot = world.map.at_id(client_bot.id)
        world.add_block(4, 4)
        world.add_block(6, 4)
        world.add_block(4, 6)
        world.add_block(6, 6)
        # world.add_block(6, 5)  # uncomment to see test fail
        world.take_forward(world_bot)
        assert not world_bot.has_block()

    def test_bot_drops_and_world_receives(self):
        world = World(10, 10)
        connection = DirectConnection(world)
        client_bot = connection.add_bot(5, 5)
        cohort = Cohort(client_bot)

        block_id = world.add_block(6, 5)
        assert (block := world.map.at_xy(6, 5)) is not None

        self.do_take(cohort, connection, client_bot)
        world_bot = world.map.at_id(client_bot.id)
        assert world_bot.has_block()
        assert world.map.at_xy(6, 5) is None

        self.do_drop(cohort, connection, client_bot, block_id)
        assert world.map.at_xy(6, 5) is block

    def do_drop(self, cohort, connection, client_bot, block_id):
        rq = [{'bot_key': client_bot.id, 'verb': 'drop', 'holding': block_id}]
        connection.run_request(cohort, rq)

    def do_take(self, cohort, connection, client_bot):
        rq1 = [{'bot_key': client_bot.id, 'verb': 'take'}]
        connection.run_request(cohort, rq1)

    def test_bot_sets_old_location(self):
        bot = Bot(10, 10)
        assert bot._old_location is None
        actions = bot.get_actions()
        assert 'step' in actions
        assert bot._old_location == Location(10, 10)

    def test_cannot_set_into_knowledge(self):
        bot = Bot(10, 10)
        with pytest.raises(AttributeError) as error:
            bot.id = 101
        assert str(error.value) == "cannot set 'id'"

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
