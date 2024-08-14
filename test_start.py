import pytest


class Biot:
    def __init__(self):
        self.location = Point(0, 0)

    def update(self, info):
        self.location = info["location"]


class BiotMap:
    pass


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))


class Entities:
    def __init__(self):
        self.contents = {}

    def place(self, biot, location):
        self.contents[location] = biot


class BiotWorld:
    def __init__(self):
        self.biots = Entities()

    def add(self, biot):
        location = Point(10, 10)
        self.biots.place(biot, location)
        return {"location": location}


class TestCase:
    def test_something(self):
        assert True is True

    def test_create_biot(self):
        biot = Biot()
        assert isinstance(biot, Biot)

    def test_starting_location(self):
        biot = Biot()
        assert biot.location == Point(0, 0)

    def test_biot_in_world(self):
        biot = Biot()
        world = BiotWorld()
        info = world.add(biot)
        point = info["location"]
        biot.update(info)
        assert biot.location == point

    @pytest.mark.skip()
    def test_create_biot_map(self):
        map = BiotMap()
