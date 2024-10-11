from bot import Bot
from direction import Direction


class DirectConnection:
    def __init__(self, world):
        self.world = world

    def add_bot(self, x, y, direction=Direction.EAST):
        bot_id = self.world.add_bot(x, y, direction)
        result_dict = self.world.fetch(bot_id)
        bot = Bot(x, y)
        bot._knowledge.update(result_dict)
        return bot

    def set_direction(self, bot, direction_string):
        self.world.command('turn', bot.id, direction_string)
        self.update_client(bot)

    def update_client(self, bot):
        result_dict = self.world.fetch(bot.id)
        bot._knowledge.update(result_dict)

    def step(self, bot):
        self.world.command('step', bot.id)
        self.update_client(bot)

    def take(self, client_bot):
        self.world.command('take', client_bot.id)
        self.update_client(client_bot)

    def drop(self, client_bot, block_id):
        self.world.command('drop', client_bot.id, block_id)
        self.update_client(client_bot)
