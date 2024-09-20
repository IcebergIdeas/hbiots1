from bot import Bot
from location import Location
from world import World


class Population:
    def __init__(self, bot_count=0):
        self._bots = []
        for i in range(bot_count):
            self._bots.append(Bot(i, i))

    def __iter__(self):
        return iter(self._bots)

    def add(self, entity):
        self._bots.append(entity)


class TestPopulation:
    def test_exists(self):
        population = Population()
        assert population is not None

    def test_has_bots(self):
        population = Population(2)
        count = 0
        for bot in population:
            count += 1
        assert count == 2


class WorldProxy:
    def __init__(self, width=20, height=20):
        self._population = Population()
        # self._world = World(width, height)
        self._world = ClientProxy(width, height)

    def add(self, entity):
        self._world.add(entity)
        entity.world = self
        self._population.add(entity)

    def run_cycle(self):
        for bot in self._population:
            bot.do_something()

    def step(self, bot):
        self._world.step(bot)




class TestWorldProxy:
    def test_exists(self):
        proxy = WorldProxy()

    def test_add_bot(self):
        proxy = WorldProxy()
        bot = Bot(5, 5)
        proxy.add(bot)
        assert bot.world == proxy

    def test_round_trip(self):
        proxy = WorldProxy()
        bot = Bot(5, 5)
        bot.direction_change_chance = 0
        proxy.add(bot)
        proxy.run_cycle()
        assert bot.location == Location(6, 5)


class ClientProxy:
    def __init__(self, width=20, height=20):
        self._world = World(width, height)

    def add(self, entity):
        self._world.add(entity)

    def step(self, bot):
        self._world.step(bot)


class TestClientProxy:
    def test_exists(self):
        proxy = ClientProxy()

    def test_add_bot(self):
        proxy = ClientProxy()
        bot = Bot(5, 5)
        proxy.add(bot)
        entity = proxy._world.map.entity_at(5, 5)
        assert entity.name == 'R'

