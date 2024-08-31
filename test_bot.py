from bot import Bot
from direction import Direction
from location import Location
from world import World


class TestBot:

    def test_step(self):
        world = World(10, 10)
        bot = Bot(5, 5)
        world.add(bot)
        location = bot.location
        bot.direction = Direction.NORTH
        bot.step()
        assert bot.location == location + Direction.NORTH
