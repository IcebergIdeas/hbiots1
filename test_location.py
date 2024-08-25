import pytest

from bot import Bot
from block import Block
from direction import Direction
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
        bot.direction = Direction.NORTH
        bot.step()
        new_point = bot.location
        assert new_point == Point(point.x, point.y + 1)

    def test_move_east(self):
        world = World(10, 10)
        bot = Bot(5, 5)
        world.add(bot)
        point = bot.location
        bot.step()
        new_point = bot.location
        assert new_point == Point(point.x + 1, point.y)

    def test_move_south(self):
        world = World(10, 10)
        bot = Bot(10, 10, Direction.SOUTH)
        world.add(bot)
        point = bot.location
        bot.step()
        new_point = bot.location
        assert new_point == Point(point.x, point.y - 1)

    def test_move_west(self):
        world = World(10, 10)
        bot = Bot(10, 10, Direction.WEST)
        world.add(bot)
        point = bot.location
        bot.step()
        new_point = bot.location
        assert new_point == Point(point.x - 1, point.y)

    def test_stop_at_edge(self):
        world = World(10, 10)
        bot = Bot(8, 5)
        world.add(bot)
        bot.step()
        bot.step()
        assert bot.location == Point(10, 5)
        bot.step()
        assert bot.location == Point(10, 5)

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
            bot.move_south()
            bot.move_west()
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
            bot.move_south()
            bot.move_west()
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

    def test_bot_notices_a_block(self):
        world = World(10, 10)
        bot = Bot(5, 5)
        world.add(bot)
        block = Block(6, 5)
        world.add(block)
        bot.do_something()
        assert bot.has(block)

    def test_take_a_block(self):
        world = World(10, 10)
        bot = Bot(5, 5)
        world.add(bot)
        block = Block(6, 5)
        world.add(block)
        bot.take()
        result = bot.scan()
        expected_scan = [('R', 5, 5)]
        assert result == expected_scan

    def test_bot_has_a_block(self):
        world = World(10, 10)
        bot = Bot(5, 5)
        world.add(bot)
        block = Block(6, 5)
        world.add(block)
        bot.take()
        assert bot.has(block)

    def test_bot_cant_take_diagonally(self):
        world = World(10, 10)
        bot = Bot(5, 5)
        world.add(bot)
        block = Block(4, 4)
        world.add(block)
        block = Block(6, 4)
        world.add(block)
        block = Block(4, 6)
        world.add(block)
        block = Block(6, 6)
        world.add(block)
        bot.take()
        assert not bot.has(block)

    def test_demo(self):
        world = World(10, 10)
        bot = Bot(5, 5)
        world.add(bot)
        block = Block(8, 5)
        world.add(block)
        print()
        self.print_result(bot)
        bot.move_east() # 6, 5
        bot.move_east() # 7, 5
        self.print_result(bot)
        bot.take()
        bot.move_south() # 7, 4
        bot.move_south() # 7, 3
        bot.move_west() # 6, 3
        bot.move_west() # 5, 3
        self.print_result(bot)
        bot.drop_south() # 5, 2
        self.print_result(bot)
        bot.move_east() # 6, 3
        bot.move_east() # 7, 3
        bot.move_north() # 7, 4
        bot.move_north() # 7, 5
        self.print_result(bot)
        bot.take()
        bot.move_south() # 7, 4
        bot.move_south() # 7, 3
        bot.move_west() # 6, 3
        self.print_result(bot)
        bot.drop_west() # 5, 3
        bot.move_east() # 7, 3
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
