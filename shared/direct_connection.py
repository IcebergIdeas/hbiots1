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

    def update_client(self, client_bot):
        result_dict = self.world.fetch(client_bot.id)
        client_bot._knowledge.update(result_dict)

    def step(self, cohort, client_bot_id):
        rq = dict()
        rq['entity'] = client_bot_id
        rq['verb'] = 'step'
        rq_list = [rq]
        self.world.execute_list(rq_list)
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

    def turn(self, cohort, client_bot_id, direction_string):
        rq = dict()
        rq['entity'] = client_bot_id
        turn_action = {'verb': 'turn', 'param1': direction_string}
        rq['actions'] = [turn_action,]
        self.world.execute(rq)
        result_dict = self.world.fetch(client_bot_id)
        cohort.update(result_dict)
