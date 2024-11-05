from client.bot import Bot
from shared.direction import Direction


class DirectConnection:
    def __init__(self, world):
        self.world = world

    def add_bot(self, x, y, direction=Direction.EAST):
        bot_id = self.world.add_bot(x, y, direction)
        result_dict = self.world.fetch(bot_id)
        client_bot = Bot(x, y)
        client_bot._knowledge.update(result_dict)
        return client_bot

    def set_direction(self, client_bot, direction_string):
        self.world.command('turn', client_bot.id, direction_string)
        self.update_client(client_bot)

    def update_client(self, client_bot):
        result_dict = self.world.fetch(client_bot.id)
        client_bot._knowledge.update(result_dict)

    def step(self, cohort, client_bot_id):
        rq = dict()
        rq['entity'] = client_bot_id
        step_action = {'verb': 'step'}
        rq['actions'] = [step_action,]
        self.world.execute(rq)
        result_dict = self.world.fetch(client_bot_id)
        cohort.update(result_dict)

    def take(self, cohort, client_bot_id):
        rq = dict()
        rq['entity'] = client_bot_id
        take_action = {'verb': 'take'}
        rq['actions'] = [take_action,]
        self.world.execute(rq)
        result_dict = self.world.fetch(client_bot_id)
        cohort.update(result_dict)

    def drop(self, cohort, client_bot_id, holding_id):
        rq = dict()
        rq['entity'] = client_bot_id
        drop_action = {'verb': 'drop', 'param1': holding_id}
        rq['actions'] = [drop_action,]
        self.world.execute(rq)
        result_dict = self.world.fetch(client_bot_id)
        cohort.update(result_dict)
