from bot import Bot
from direction import Direction
from location import Location
from world import World


class Queue:
    def __init__(self):
        self._contents = []

    def put(self, item):
        self._contents.append(item)

    def get(self):
        return self._contents.pop(0)


class TestPathing:
    def test_hookup(self):
        assert 2 + 2 == 4

    def test_queue(self):
        q = Queue()
        q.put(2)
        assert q.get() == 2

    def test_queue_more(self):
        q = Queue()
        q.put(2)
        q.put(5)
        assert q.get() == 2
        assert q.get() == 5

    def test_simple_path(self):
        target = Location(10, 10)
        start = Location(5, 5)
        d = start.distance(target)
        for step in range(d):
            start = start.step_toward(target)
        assert start == target

    def test_wandering(self):
        world = World(10, 10)
        bot = Bot(5, 5)
        world.add(bot)
        bot.do_something()
        loc = bot.location
        assert loc != Location(5, 5)

    def test_changes_direction(self):
        world = World(10, 10)
        bot = Bot(9, 5)
        bot.direction_change_chance = 0.0
        world.add(bot)
        bot.do_something()
        assert bot.location == Location(10, 5)
        bot.do_something()
        assert bot.location == Location(10, 5)
        assert bot.direction != Direction.EAST
        bot.do_something()
        assert bot.location != Location(10, 5)
