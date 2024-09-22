from world import World


class Connection:
    def __init__(self, world):
        self.world = world


class TestConnection:
    def test_exists(self):
        world = World(20, 20)
        connection = Connection(world)