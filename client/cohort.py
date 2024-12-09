from typing import Callable


class Cohort:
    def __init__(self, bot=None):
        self.bots = {}
        if bot:
            self.bots[bot.key] = bot
        self.clear_bot_creation()

    # noinspection PyAttributeOutsideInit
    def clear_bot_creation(self):
        self._bots_to_add = 0
        self._callback = None

    def add_bots(self, number, callback: Callable[[int, int], tuple[int, int, str]]):
        self._bots_to_add += number
        self._callback = callback

    def create_message(self):
        message = []
        self.add_desired_bots(message)
        self.get_existing_bot_actions(message)
        return message

    def add_desired_bots(self, message):
        for i in range(self._bots_to_add):
            x, y, d = self._callback(i, self._callback)
            action = {'bot_key': 0,
                      'verb': 'add_bot',
                      'x': x,
                      'y': y,
                      'direction': d
                      }
            message.append(action)
        self.clear_bot_creation()

    def get_existing_bot_actions(self, message):
        for bot in self.bots.values():
            actions = bot.get_actions()
            for verb in actions:
                action = self.create_action(bot, verb)
                message.append(action)

    def create_action(self, bot, verb):
        match verb:
            case 'drop':
                return {'bot_key': bot.key, 'verb': verb, 'holding': bot.holding}
            case _:
                return {'bot_key': bot.key, 'verb': verb}

    def update(self, results):
        for result_dict in results['updates']:
            bot_id = result_dict['key']
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
        self.bots[bot_id] = new_bot
        return new_bot
