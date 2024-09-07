
class FakeBot:
    def __init__(self):
        self.inventory = None
        self.location = None

    def receive(self, item):
        self.inventory = item

    def set_location(self, location):
        self.location = location


class WorldFacade:
    def __init__(self, target):
        self.target = target
        self.actions = []

    def take(self):
        self.actions.append("take")

    def move(self):
        self.actions.append("move")

    def unwind(self):
        """
        The network stuff is in here. We would send these messages to World,
        and it would send others back, through its own Facade thing.
        """
        for action in self.actions:
            match action:
                case "take":
                    self.target.receive('entity')
                case "move":
                    self.target.set_location((10, 10))



class TestCSSpike:
    def test_hookup(self):
        assert 2 + 2 == 4

    def test_simple_scenario(self):
        target = FakeBot()
        wf = WorldFacade(target)
        wf.take()
        wf.move()
        wf.unwind()
        assert target.inventory == "entity"
        assert target.location == (10, 10)