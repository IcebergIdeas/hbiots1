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

    def run_request(self, cohort, rq):
        results = self.world.execute_requests(rq)
        cohort.update(results['updates'])
