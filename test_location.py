import pytest

from bot import Bot
from block import Block
from world import World
from point import Point


class TestLocation:
    def test_something(self):
        assert True is True

    def test_create_bot(self):
        bot = Bot(10, 10)
        assert isinstance(bot, Bot)

    def test_starting_location(self):
        bot = Bot(10, 10)
        assert bot.location == Point(10, 10)

    def test_bot_in_world(self):
        bot = Bot(10, 10)
        world = World()
        world.add(bot)
        point = Point(10, 10)
        assert bot.id == 101
        assert bot.location == point

    def test_move_north(self):
        world = World()
        bot = Bot(10, 10)
        world.add(bot)
        point = bot.location
        world.move_north(bot)
        new_point = bot.location
        assert new_point == Point(point.x, point.y + 1)

    def test_move_east(self):
        world = World()
        bot = Bot(10, 10)
        world.add(bot)
        point = bot.location
        world.move_east(bot)
        new_point = bot.location
        assert new_point == Point(point.x + 1, point.y)

    def test_move_south(self):
        world = World()
        bot = Bot(10, 10)
        world.add(bot)
        point = bot.location
        world.move_south(bot)
        new_point = bot.location
        assert new_point == Point(point.x, point.y - 1)

    def test_move_west(self):
        world = World()
        bot = Bot(10, 10)
        world.add(bot)
        point = bot.location
        world.move_west(bot)
        new_point = bot.location
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

    def test_draw_world_with_bot(self):
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
        bot = Bot(10, 10)
        world.add(bot)
        for _ in range(5):
            world.move_south(bot)
            world.move_west(bot)
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
        bot = Bot(10, 10)
        world.add(bot)
        for _ in range(5):
            world.move_south(bot)
            world.move_west(bot)
        block = Block(8, 5)
        world.add(block)
        drawing = world.draw()
        assert drawing == expected

    def test_scan(self):
        world = World()
        bot = Bot(10, 10)
        world.add(bot)
        result = bot.scan()
        expected_scan = [('R', 10, 10)]
        assert result == expected_scan

    def test_scan_a_block(self):
        world = World()
        bot = Bot(5, 5)
        world.add(bot)
        block = Block(6, 5)
        world.add(block)
        result = bot.scan()
        expected_scan = [('R', 5, 5), ('B', 6, 5)]
        assert result == expected_scan
