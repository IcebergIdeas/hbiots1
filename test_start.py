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

    def test_move(self):
        world = BiotWorld()
        biot = Biot()
        info = world.add(biot)
        biot.update(info)
        point = info["location"]
        assert biot.id == 101
        new_info = world.move(biot.id, 10, 0)
        biot.update(new_info)
        new_point = biot.location
        assert new_point == Point(point.x+10, point.y)

