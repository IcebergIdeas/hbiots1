import copy

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
        bot = world.add_bot(10, 10)
        connection = DirectConnection(world)
        connection.step(bot)
        assert bot.location == Location(11, 10)
        assert world.map.at_xy(11, 10).id == bot.id

    def test_step_north(self):
        world = World(10, 10)
        client_bot = world.add_bot(5, 5, Direction.NORTH)
        location = client_bot.location
        connection = DirectConnection(world)
        connection.step(client_bot)
        assert client_bot.location == location + Direction.NORTH
