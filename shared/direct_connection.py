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
        rq = [ {'entity': client_bot_id, 'verb': 'step', 'param1': None}]
        self.run_request(cohort, client_bot_id, rq)

    def take(self, cohort, client_bot_id):
        rq = [ {'entity': client_bot_id, 'verb': 'take', 'param1': None}]
        self.run_request(cohort, client_bot_id, rq)

    def drop(self, cohort, client_bot_id, holding_id):
        rq = [ {'entity': client_bot_id, 'verb': 'drop', 'param1': holding_id}]
        self.run_request(cohort, client_bot_id, rq)

    def turn(self, cohort, client_bot_id, direction_string):
        rq = [ { 'entity': client_bot_id, 'verb': 'turn', 'param1': direction_string}]
        self.run_request(cohort, client_bot_id, rq)

    def run_request(self, cohort, client_bot_id, rq):
        results = self.world.execute(rq)
        cohort.update(results)
