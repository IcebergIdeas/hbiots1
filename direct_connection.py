import copy



class DirectConnection:
    def __init__(self, world):
        self.world = world

    def add_bot(self, x, y):
        from bot import Bot
        id = self.world.add_world_bot(x, y)
        client_bot = Bot(x, y)
        client_bot.id = id
        client_bot.world = self.world
        result = self.world.fetch(id)
        client_bot._knowledge = copy.copy(result)
        return client_bot

    def set_direction(self, bot, direction_string):
        self.world.command('turn', bot.id, direction_string)
        result = self.world.fetch(bot.id)
        bot._knowledge = copy.copy(result)

    def step(self, bot):
        self.world.command('step', bot.id)
        result = self.world.fetch(bot.id)
        bot._knowledge = copy.copy(result)

    def take(self, client_bot):
        self.world.command('take', client_bot.id)
        result = self.world.fetch(client_bot.id)
        client_bot._knowledge = copy.copy(result)

    def drop(self, client_bot, block):
        self.world.command('drop', client_bot.id, block.id)
        result = self.world.fetch(client_bot.id)
        client_bot._knowledge = copy.copy(result)
