import pytest

from client.bot import Bot
from client.cohort import Cohort
from server.world_entity import WorldEntity
from shared.direction import Direction
from shared.location import Location


class FakeBot:
    def __init__(self, key):
        self.key = key
        self.actions = []

    def do(self, actions):
        self.actions = actions

    @property
    def holding(self):
        return 666

    def get_actions(self):
        return self.actions


class TestCohort:
    def test_hookup(self):
        assert True

    def test_cohort(self):
        bot = Bot(5, 5)
        bot.direction_change_chance = 0
        cohort = Cohort(bot)
        message = cohort.create_message()
        assert len(message) == 1
        assert message[0]['verb'] == 'step'
        assert message[0]['bot_key'] == bot.key

    def test_really_tricky_bot(self):
        bot = FakeBot(101)
        bot.do(['step', 'take', 'drop'])
        cohort = Cohort(bot)
        message = cohort.create_message()
        assert len(message) == 3
        assert message[0] == {'verb': 'step', 'bot_key': 101}
        assert message[1] == {'verb': 'take', 'bot_key': 101}
        assert message[2] == {'verb': 'drop', 'bot_key': 101, 'holding': 666}

    def test_bot_turning(self):
        bot = FakeBot(101)
        bot.do(['NORTH', 'EAST', 'SOUTH', 'WEST'])
        cohort = Cohort(bot)
        message = cohort.create_message()
        assert len(message) == 4
        assert message[0] == {'verb': 'NORTH', 'bot_key': 101}
        assert message[1] == {'verb': 'EAST', 'bot_key': 101}
        assert message[2] == {'verb': 'SOUTH', 'bot_key': 101}
        assert message[3] == {'verb': 'WEST', 'bot_key': 101}

    def test_adding_via_surprise_knowledge(self):
        cohort = Cohort()
        WorldEntity.next_key = 100
        new_bot = WorldEntity.bot(5, 6, Direction.EAST)
        dict = new_bot.as_dictionary()
        updates = [ dict ]
        messages = []
        results = { 'messages': messages, 'updates': updates }
        cohort.update(results)
        client_bot = cohort.bots[new_bot.key]
        assert client_bot.location == Location(5, 6)

    def test_adding_bots(self):
        def callback(i, n):
            return bot_values[i]

        bot_values =  [
            (5, 10, 'EAST'),
            (10, 17, 'NORTH'),
            (31, 93, 'WEST'),
            (73, 87, 'WEST'),
            (37, 23, 'SOUTH'),
        ]
        cohort = Cohort()
        cohort.add_bots(5, callback)
        message = cohort.create_message()
        assert len(message) == 5
        for index, msg in enumerate(message):
            assert msg['verb'] == 'add_bot'
            assert msg['x'] == bot_values[index][0]
            assert msg['y'] == bot_values[index][1]
            assert msg['direction'] == bot_values[index][2]
        assert cohort._bots_to_add == 0

    def test_add_error_wrong_return(self):
        cohort = Cohort()
        cohort.add_bots(5, lambda i, n:( 5, 6))
        with pytest.raises(ValueError) as error:
            message = cohort.create_message()
        assert str(error.value) == 'not enough values to unpack (expected 3, got 2)'

    def test_can_drop(self):
        # invasive to cover missing forwarder
        cohort = Cohort()
        test_bot = Bot(5, 5, Direction.EAST)
        test_bot._knowledge.key = 101
        test_bot._knowledge._held_entity = 666
        action = cohort.create_action(test_bot, 'drop')
        assert action['verb'] == 'drop'
        assert action['bot_key'] == test_bot.key
        assert action['holding'] == 666




