

class Cohort:
    def __init__(self, bot=None):
        self.bots = {}
        if bot:
            self.bots[bot.id] = bot
        self._bots_to_add = 0

    def add_bots(self, number):
        self._bots_to_add += number

    def create_message(self):
        message = []
        self.add_desired_bots(message)
        self.get_existing_bot_actions(message)
        return message

    def add_desired_bots(self, message):
        for _ in range(self._bots_to_add):
            action = {'entity': 0, 'verb': 'add_bot'}
            message.append(action)
        self._bots_to_add = 0

    def get_existing_bot_actions(self, message):
        for bot in self.bots.values():
            actions = bot.get_actions()
            for verb in actions:
                action = self.create_action(bot, verb)
                message.append(action)

    def create_action(self, bot, verb):
        match verb:
            case 'drop':
                return {'entity': bot.id, 'verb': verb, 'holding': bot.holding}
            case _:
                return {'entity': bot.id, 'verb': verb}

    def update(self, results):
        for result_dict in results:
            bot_id = result_dict['eid']
            bot = self.by_id(bot_id)
            bot.update(result_dict)

    def by_id(self, bot_id):
        try:
            return self.bots[bot_id]
        except KeyError:
            return self._create_new_bot(bot_id)

    def _create_new_bot(self, bot_id):
        from client.bot import Bot
        new_bot = Bot(0, 0)
        new_bot.id = bot_id
        self.bots[bot_id] = new_bot
        return new_bot
