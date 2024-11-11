from client.bot import Bot, Cohort


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
