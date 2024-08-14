import pytest


class Biot:
    def __init__(self):
        self.location = Point(0, 0)


class BiotMap:
    pass


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


class TestCase:
    def test_something(self):
        assert True is True

    def test_create_biot(self):
        biot = Biot()
        assert isinstance(biot, Biot)

    def test_starting_location(self):
        biot = Biot()
        assert biot.location == Point(0, 0)

    @pytest.mark.skip()
    def test_create_biot_map(self):
        map = BiotMap()
