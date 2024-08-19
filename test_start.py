import pytest

from biot import Biot
from block import Block
from world import World
from point import Point


class TestCase:
    def test_something(self):
        assert True is True

    def test_create_biot(self):
        biot = Biot()
        assert isinstance(biot, Biot)

    def test_starting_location(self):
        biot = Biot()
        assert biot.location is None

    def test_biot_in_world(self):
        biot = Biot()
        world = World()
        world.add(biot)
        point = Point(10, 10)
        assert biot.id == 101
        assert biot.location == point

    def test_move_north(self):
        world = World()
        biot = Biot()
        world.add(biot)
        point = biot.location
        world.move_north(biot)
        new_point = biot.location
        assert new_point == Point(point.x, point.y + 1)

    def test_move_east(self):
        world = World()
        biot = Biot()
        world.add(biot)
        point = biot.location
        world.move_east(biot)
        new_point = biot.location
        assert new_point == Point(point.x + 1, point.y)

    def test_move_south(self):
        world = World()
        biot = Biot()
        world.add(biot)
        point = biot.location
        world.move_south(biot)
        new_point = biot.location
        assert new_point == Point(point.x, point.y - 1)

    def test_move_west(self):
        world = World()
        biot = Biot()
        world.add(biot)
        point = biot.location
        world.move_west(biot)
        new_point = biot.location
        assert new_point == Point(point.x - 1, point.y)

    def test_draw_empty_world(self):
        expected = \
            '__________\n' \
            '__________\n' \
            '__________\n' \
            '__________\n' \
            '__________\n' \
            '__________\n' \
            '__________\n' \
            '__________\n' \
            '__________\n' \
            '__________\n'
        world = World()
        drawing = world.draw()
        assert drawing == expected

    def test_draw_world_with_biot(self):
        expected = \
            '__________\n' \
            '__________\n' \
            '__________\n' \
            '__________\n' \
            '__________\n' \
            '_____R____\n' \
            '__________\n' \
            '__________\n' \
            '__________\n' \
            '__________\n'
        world = World()
        biot = Biot()
        world.add(biot)
        for _ in range(5):
            world.move_south(biot)
            world.move_west(biot)
        drawing = world.draw()
        assert drawing == expected

    def test_draw_world_with_second_entity(self):
        expected = \
            '__________\n' \
            '__________\n' \
            '__________\n' \
            '__________\n' \
            '__________\n' \
            '_____R__B_\n' \
            '__________\n' \
            '__________\n' \
            '__________\n' \
            '__________\n'
        world = World()
        biot = Biot()
        world.add(biot)
        for _ in range(5):
            world.move_south(biot)
            world.move_west(biot)
        block = Block(8, 5)
        world.add(block)
        drawing = world.draw()
        assert drawing == expected
