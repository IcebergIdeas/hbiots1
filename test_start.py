import pytest

from biot import Biot
from biot_world import BiotWorld
from point import Point


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
