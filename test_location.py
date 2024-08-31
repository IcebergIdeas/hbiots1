import pytest

from bot import Bot
from block import Block
from direction import Direction
from world import World
from location import Location


class TestLocation:
    def test_something(self):
        assert True is True

    def test_create_bot(self):
        bot = Bot(10, 10)
        assert isinstance(bot, Bot)

    def test_starting_location(self):
        bot = Bot(10, 10)
        assert bot.location == Location(10, 10)

    def test_bot_in_world(self):
        bot = Bot(10, 10)
        world = World(10, 10)
        world.add(bot)
        point = Location(10, 10)
        assert bot.id == 101
        assert bot.location == point

    def test_location_plus_direction_math(self):
        location = Location(5, 5)
        assert location + Direction.NORTH == Location(5, 4)
        assert location + Direction.SOUTH == Location(5, 6)
        assert location + Direction.EAST == Location(6, 5)
        assert location + Direction.WEST == Location(4, 5)

    @pytest.mark.skip("needs to exist")
    def test_world_deals_with_location_at_edge(self):
        pass

    @pytest.mark.skip("needs to exist")
    def test_bot_gets_updated(self):
        pass

    def test_move_north(self):
        world = World(10, 10)
        bot = Bot(5, 5)
        world.add(bot)
        point = bot.location
        bot.direction = Direction.NORTH
        bot.step()
        new_point = bot.location
        assert new_point == Location(point.x, point.y - 1)

    def test_move_east(self):
        world = World(10, 10)
        bot = Bot(5, 5)
        world.add(bot)
        point = bot.location
        bot.step()
        new_point = bot.location
        assert new_point == Location(point.x + 1, point.y)

    def test_move_south(self):
        world = World(10, 10)
        bot = Bot(10, 9, Direction.SOUTH)
        world.add(bot)
        point = bot.location
        bot.step()
        new_point = bot.location
        assert new_point == Location(point.x, point.y + 1)

    def test_move_west(self):
        world = World(10, 10)
        bot = Bot(10, 10, Direction.WEST)
        world.add(bot)
        point = bot.location
        bot.step()
        new_point = bot.location
        assert new_point == Location(point.x - 1, point.y)

    def test_stop_at_edge(self):
        world = World(10, 10)
        bot = Bot(8, 5)
        world.add(bot)
        bot.step()
        bot.step()
        assert bot.location == Location(10, 5)
        bot.step()
        assert bot.location == Location(10, 5)

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

    @pytest.mark.skip("later")
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
            bot.direction = Direction.SOUTH
            bot.step()
            bot.direction = Direction.WEST
            bot.step()
        drawing = world.draw()
        assert drawing == expected

    @pytest.mark.skip("later")
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
            bot.direction = Direction.SOUTH
            bot.step()
            bot.direction = Direction.WEST
            bot.step()
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
        bot.tired = 0
        bot.direction_change_chance = 0
        world.add(bot)
        block = Block(7, 5)
        world.add(block)
        bot.do_something()
        assert bot.state == "looking"
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

    def test_bot_facing_north_takes_a_north_block(self):
        world = World(10, 10)
        bot = Bot(5, 5)
        world.add(bot)
        block = Block(5, 4)
        world.add(block)
        bot.direction = Direction.NORTH
        bot.take()
        assert bot.has(block)

    def test_bot_facing_east_takes_an_east_block(self):
        world = World(10, 10)
        bot = Bot(5, 5)
        world.add(bot)
        block = Block(6, 5)
        world.add(block)
        bot.take()
        assert bot.has(block)

    def test_bot_facing_south_takes_a_south_block(self):
        world = World(10, 10)
        bot = Bot(5, 5)
        world.add(bot)
        block = Block(5, 6)
        world.add(block)
        bot.direction = Direction.SOUTH
        bot.take()
        assert bot.has(block)

    def test_bot_facing_west_takes_a_west_block(self):
        world = World(10, 10)
        bot = Bot(5, 5)
        world.add(bot)
        block = Block(4, 5)
        world.add(block)
        bot.direction = Direction.WEST
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

    def test_bot_cannot_drop_off_world_north(self):
        world = World(10, 10)
        bot = Bot(5, 0)
        block = Block(4, 4)
        bot.receive(block)
        bot.direction = Direction.NORTH
        world.drop_forward(bot, block)
        assert bot.has(block), 'drop should not happen'

    def test_bot_cannot_drop_off_world_east(self):
        world = World(10, 10)
        bot = Bot(10, 5)
        block = Block(4, 4)
        bot.receive(block)
        bot.direction = Direction.EAST
        world.drop_forward(bot, block)
        assert bot.has(block), 'drop should not happen'

    def test_bot_cannot_drop_off_world_south(self):
        world = World(10, 10)
        bot = Bot(5, 10)
        block = Block(4, 4)
        bot.receive(block)
        bot.direction = Direction.SOUTH
        world.drop_forward(bot, block)
        assert bot.has(block), 'drop should not happen'

    def test_bot_cannot_drop_off_world_west(self):
        world = World(10, 10)
        bot = Bot(0, 5)
        block = Block(4, 4)
        bot.receive(block)
        bot.direction = Direction.WEST
        world.drop_forward(bot, block)
        assert bot.has(block), 'drop should not happen'


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
