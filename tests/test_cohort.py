from client.bot import Bot, Cohort


class FakeBot:
    def __init__(self, id):
        self.id = id
        self.actions = []

    def do(self, actions):
        self.actions = actions

    @property
    def holding(self):
        return 666

    def do_something(self, _connection):
        return self.actions


class TestCohort:
    def test_hookup(self):
        assert True

    def test_cohort(self):
        bot = Bot(5, 5)
        bot.id = 101
        bot.direction_change_chance = 0
        cohort = Cohort(bot)
        message = cohort.create_message()
        assert len(message) == 1
        assert message[0]['verb'] == 'step'
        assert message[0]['entity'] == 101

    def test_really_tricky_bot(self):
        bot = FakeBot(101)
        bot.do(['step', 'take', 'drop'])
        cohort = Cohort(bot)
        message = cohort.create_message()
        assert len(message) == 3
        assert message[0] == {'verb': 'step', 'entity': 101}
        assert message[1] == {'verb': 'take', 'entity': 101}
        assert message[2] == {'verb': 'drop', 'entity': 101, 'param1': 666}

    def test_bot_turning(self):
        bot = FakeBot(101)
        bot.do(['NORTH', 'EAST', 'SOUTH', 'WEST'])
        cohort = Cohort(bot)
        message = cohort.create_message()
        assert len(message) == 4
        assert message[0] == {'verb': 'turn', 'param1':'NORTH', 'entity': 101}
        assert message[1] == {'verb': 'turn', 'param1':'EAST', 'entity': 101}
        assert message[2] == {'verb': 'turn', 'param1':'SOUTH', 'entity': 101}
        assert message[3] == {'verb': 'turn', 'param1':'WEST', 'entity': 101}


