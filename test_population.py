from bot import Bot
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
        self._world = World(width, height)

    def add(self, entity):
        self._world.add(entity)
        entity.world = self
        self._population.add(entity)




class TestWorldProxy:
    def test_exists(self):
        proxy = WorldProxy()

    def test_add_bot(self):
        proxy = WorldProxy()
        bot = Bot(5, 5)
        proxy.add(bot)
        assert bot.world == proxy