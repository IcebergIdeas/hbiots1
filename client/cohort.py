

class Cohort:
    def __init__(self, bot=None):
        self.bots = {}
        if bot:
            self.bots[bot.id] = bot

    def create_message(self):
        message = []
        for bot in self.bots.values():
            actions = bot.get_actions()
            for verb in actions:
                action = self.create_action(bot, verb)
                message.append(action)
        return message

    def create_action(self, bot, verb):
        match verb:
            case 'drop':
                return {'entity': bot.id, 'verb': verb, 'holding': bot.holding}
            case 'NORTH' | 'EAST' | 'SOUTH' | 'WEST' as direction:
                return {'entity': bot.id, 'verb': 'turn', 'direction': direction}
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
            return self.create_new_bot(bot_id)

    def create_new_bot(self, bot_id):
        from client.bot import Bot
        new_bot = Bot(0, 0)
        new_bot.id = bot_id
        self.bots[bot_id] = new_bot
        return new_bot
