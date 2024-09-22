from bot import Bot
from location import Location
from world import World


class DirectConnection:
    def __init__(self, world):
        self.world = world

    def step(self, bot):
        self.knowledge = bot._knowledge
        self.world.step(self.knowledge)


class TestConnection:
    def test_exists(self):
        world = World(20, 20)
        connection = DirectConnection(world)

    def test_step(self):
        world = World(20, 20)
        bot = Bot(10, 10)
        world.add(bot)
        connection = DirectConnection(world)
        connection.step(bot)
        assert connection.knowledge.location == Location(11, 10)
        assert world.map.entity_at(11, 10) == bot
