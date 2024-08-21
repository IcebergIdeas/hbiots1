from bot import Bot
from point import Point
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
        target = Point(10, 10)
        start = Point(5, 5)
        d = start.distance(target)
        for step in range(d):
            start = start.step_toward(target)
        assert start == target

    def test_stop_at_edge(self):
        world = World(10, 10)
        bot = Bot(8, 5)
        world.add(bot)
        world.move_east(bot)
        world.move_east(bot)
        assert bot.location == Point(10, 5)
        world.move_east(bot)
        assert bot.location == Point(10, 5)

    def test_wandering(self):
        world = World(10, 10)
        bot = Bot(5, 5)
        world.add(bot)
        bot.do_something()
        loc = bot.location
        assert loc != Point(5, 5)

    def test_changes_direction(self):
        world = World(10, 10)
        bot = Bot(9, 5)
        bot.direction_change_chance = 0.0
        world.add(bot)
        bot.do_something()
        assert bot.location == Point(10, 5)
        bot.do_something()
        assert bot.location != Point(10, 5)


