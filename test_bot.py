from block import Block
from bot import Bot
from direction import Direction
from knowledge import Knowledge
from location import Location
from machine import Looking
from map import Map
from world import World


class TestBot:
    # Seems to have redundant tests, needs cleanup

    def test_create_bot(self):
        bot = Bot(10, 10)
        assert isinstance(bot, Bot)

    def test_starting_location(self):
        bot = Bot(10, 10)
        assert bot.location == Location(10, 10)

    def test_bot_in_world(self):
        World.next_id = 100
        bot = Bot(10, 10)
        world = World(10, 10)
        world.add(bot)
        point = Location(10, 10)
        assert bot.id == 101
        assert bot.location == point

    def test_bot_facing_north_block(self):
        map = Map(10, 10)
        bot = Bot(5, 5)
        bot.direction = Direction.NORTH
        map.place(bot)
        bot.vision = map.vision_at(bot.location)
        assert not bot.can_take()
        map.place(Block(5,4))
        bot.vision = map.vision_at(bot.location)
        assert bot.can_take()

    def test_bot_facing_east_block(self):
        map = Map(10, 10)
        bot = Bot(5, 5)
        bot.direction = Direction.EAST
        map.place(bot)
        bot.vision = map.vision_at(bot.location)
        assert not bot.can_take()
        map.place(Block(6,5))
        bot.vision = map.vision_at(bot.location)
        assert bot.can_take()

    def test_wandering(self):
        world = World(10, 10)
        bot = Bot(5, 5)
        world.add(bot)
        bot.do_something()
        loc = bot.location
        assert loc != Location(5, 5)

    def test_changes_direction(self):
        world = World(10, 10)
        bot = Bot(9, 5)
        bot.direction_change_chance = 0.0
        world.add(bot)
        bot.do_something()
        assert bot.location == Location(10, 5)
        bot.do_something()
        assert bot.location == Location(10, 5)
        assert bot.direction != Direction.EAST
        bot.do_something()
        assert bot.location != Location(10, 5)

    def test_stop_at_edge(self):
        world = World(10, 10)
        bot = Bot(9, 5)
        world.add(bot)
        bot.step()
        assert bot.location == Location(10, 5)
        bot.step()
        assert bot.location == Location(10, 5)

# Some of these are redundant, moved from another file

    def test_bot_notices_a_block(self):
        world = World(10, 10)
        bot = Bot(5, 5)
        bot.state._energy = Knowledge.energy_threshold
        bot.direction_change_chance = 0
        world.add(bot)
        block = Block(7, 5)
        world.add(block)
        world.set_bot_vision(bot)
        bot.do_something()
        assert isinstance(bot.state, Looking)
        bot.do_something()
        assert bot.has(block)

    def test_take_a_block(self):
        world = World(10, 10)
        bot = Bot(5, 5)
        world.add(bot)
        block = Block(6, 5)
        world.add(block)
        assert not world.is_empty(Location(6, 5))
        world.take_forward(bot)
        assert bot.has(block)
        assert world.is_empty(Location(6, 5))

    def test_bot_facing_north_takes_a_north_block(self):
        world = World(10, 10)
        bot = Bot(5, 5)
        world.add(bot)
        block = Block(5, 4)
        world.add(block)
        bot.direction = Direction.NORTH
        world.take_forward(bot)
        assert bot.has(block)

    def test_bot_facing_east_takes_an_east_block(self):
        world = World(10, 10)
        bot = Bot(5, 5)
        world.add(bot)
        block = Block(6, 5)
        world.add(block)
        world.take_forward(bot)
        assert bot.has(block)

    def test_bot_facing_south_takes_a_south_block(self):
        world = World(10, 10)
        bot = Bot(5, 5)
        world.add(bot)
        block = Block(5, 6)
        world.add(block)
        bot.direction = Direction.SOUTH
        world.take_forward(bot)
        assert bot.has(block)

    def test_bot_facing_west_takes_a_west_block(self):
        world = World(10, 10)
        bot = Bot(5, 5)
        world.add(bot)
        block = Block(4, 5)
        world.add(block)
        bot.direction = Direction.WEST
        world.take_forward(bot)
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
        world.take_forward(bot)
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
