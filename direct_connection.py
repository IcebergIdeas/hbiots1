class DirectConnection:
    def __init__(self, world):
        self.world = world

    def add_bot(self, x, y):
        from bot import Bot
        id = self.world.add_world_bot(x, y)
        client_bot = Bot(x, y)
        client_bot.id = id
        client_bot.world = self.world
        self.update_client(client_bot)
        return client_bot

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

    def drop(self, client_bot, block):
        self.world.command('drop', client_bot.id, block.id)
        self.update_client(client_bot)
