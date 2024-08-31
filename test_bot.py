from bot import Bot
from direction import Direction
from location import Location
from world import World


class TestBot:

    def test_move_north(self):
        world = World(10, 10)
        bot = Bot(5, 5)
        world.add(bot)
        point = bot.location
        bot.direction = Direction.NORTH
        bot.step()
        new_point = bot.location
        assert new_point == Location(point.x, point.y - 1)
