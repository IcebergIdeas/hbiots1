import copy

from bot import Bot
from direction import Direction
from location import Location
from world import World


class DirectConnection:
    def __init__(self, world):
        self.world = world

    def step(self, bot):
        self.world.command('step', bot.id)
        result = self.world.fetch(bot.id)
        bot._knowledge = copy.copy(result)


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
        assert bot.location == Location(11, 10)
        assert world.map.at_xy(11, 10) == bot

    def test_step_north(self):
        world = World(10, 10)
        bot = Bot(5, 5)
        world.add(bot)
        location = bot.location
        bot.direction = Direction.NORTH
        connection = DirectConnection(world)
        connection.step(bot)
        assert bot.location == location + Direction.NORTH
