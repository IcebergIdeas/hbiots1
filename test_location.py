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
        world = World(10, 10)
        world.add(bot)
        point = Point(10, 10)
        assert bot.id == 101
        assert bot.location == point

    def test_move_north(self):
        world = World(10, 10)
        bot = Bot(5, 5)
        world.add(bot)
        point = bot.location
        world.move_north(bot)
        new_point = bot.location
        assert new_point == Point(point.x, point.y + 1)

    def test_move_east(self):
        world = World(10, 10)
        bot = Bot(5, 5)
        world.add(bot)
        point = bot.location
        world.move_east(bot)
        new_point = bot.location
        assert new_point == Point(point.x + 1, point.y)

    def test_move_south(self):
        world = World(10, 10)
        bot = Bot(10, 10)
        world.add(bot)
        point = bot.location
        world.move_south(bot)
        new_point = bot.location
        assert new_point == Point(point.x, point.y - 1)

    def test_move_west(self):
        world = World(10, 10)
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
        world = World(10, 10)
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
        world = World(10, 10)
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
        world = World(10, 10)
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
        world = World(10, 10)
        bot = Bot(10, 10)
        world.add(bot)
        result = bot.scan()
        expected_scan = [('R', 10, 10)]
        assert result == expected_scan

    def test_scan_a_block(self):
        world = World(10, 10)
        bot = Bot(5, 5)
        world.add(bot)
        block = Block(6, 5)
        world.add(block)
        result = bot.scan()
        expected_scan = [('R', 5, 5), ('B', 6, 5)]
        assert result == expected_scan

    def test_take_a_block(self):
        world = World(10, 10)
        bot = Bot(5, 5)
        world.add(bot)
        block = Block(6, 5)
        world.add(block)
        world.take_east(bot)
        result = bot.scan()
        expected_scan = [('R', 5, 5)]
        assert result == expected_scan

    def test_bot_gets_a_block(self):
        world = World(10, 10)
        bot = Bot(5, 5)
        world.add(bot)
        block = Block(6, 5)
        world.add(block)
        world.take_east(bot)
        assert bot.has(block)

    def test_demo(self):
        world = World(10, 10)
        bot = Bot(5, 5)
        world.add(bot)
        block = Block(8, 5)
        world.add(block)
        print()
        self.print_result(bot)
        world.move_east(bot) # 6, 5
        world.move_east(bot) # 7, 5
        self.print_result(bot)
        world.take_east(bot)
        world.move_south(bot) # 7, 4
        world.move_south(bot) # 7, 3
        world.move_west(bot) # 6, 3
        world.move_west(bot) # 5, 3
        self.print_result(bot)
        world.drop_south(bot) # 5, 2
        self.print_result(bot)
        world.move_east(bot) # 6, 3
        world.move_east(bot) # 7, 3
        world.move_north(bot) # 7, 4
        world.move_north(bot) # 7, 5
        self.print_result(bot)
        world.take_east(bot)
        world.move_south(bot) # 7, 4
        world.move_south(bot) # 7, 3
        world.move_west(bot) # 6, 3
        self.print_result(bot)
        world.drop_west(bot) # 5, 3
        world.move_east(bot) # 7, 3
        self.print_result(bot)
        assert True

    def print_result(self, bot):
        result = bot.scan()
        print_map(result)


def print_map(result):
    print()
    r = ''
    for y in range(9, -1, - 1):
        r += f'{y:2d} '
        for x in range(10):
            name = '_'
            for e in result:
                ename, ex, ey = e
                if ex == x and ey == y:
                    name = ename
            r += name
        r += '\n'
    print(r)
