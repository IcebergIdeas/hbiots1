from direction import Direction
from location import Location
from world import World
from world_entity import WorldEntity

class TestWorld:

    def test_take_a_block(self):
        world = World(10, 10)
        bot_id = world.add_bot(5, 5)
        world.add_block(6, 5)
        assert not world.is_empty(Location(6, 5))
        bot = world.entity_from_id(bot_id)
        world.take_forward(bot)
        assert bot.has_block()
        assert world.is_empty(Location(6, 5))

    def test_bot_facing_north_takes_a_north_block(self):
        self.check_directional_take((5, 4), Direction.NORTH)

    def test_bot_facing_east_takes_an_east_block(self):
        self.check_directional_take((6, 5), Direction.EAST)

    def test_bot_facing_south_takes_a_south_block(self):
        self.check_directional_take((5, 6), Direction.SOUTH)

    def test_bot_facing_west_takes_a_west_block(self):
        self.check_directional_take((4, 5), Direction.WEST)

    def check_directional_take(self, block_loc, direction):
        block_x, block_y = block_loc
        world = World(10, 10)
        bot_id = world.add_bot(5, 5, direction)
        bot = world.entity_from_id(bot_id)
        world.add_block(block_x, block_y)
        world.take_forward(bot)
        assert bot.has_block()

    def test_bot_cannot_drop_off_world_north(self):
        self.check_cannot_drop_off_world(5, 0, Direction.NORTH)

    def test_bot_cannot_drop_off_world_east(self):
        self.check_cannot_drop_off_world(10, 5, Direction.EAST)

    def test_bot_cannot_drop_off_world_south(self):
        self.check_cannot_drop_off_world(5, 10, Direction.SOUTH)

    def test_bot_cannot_drop_off_world_west(self):
        self.check_cannot_drop_off_world(0, 5, Direction.WEST)

    def check_cannot_drop_off_world(self, x, y, direction):
        world = World(10, 10)
        bot_id = world.add_bot(x, y, direction)
        bot = world.entity_from_id(bot_id)
        block = WorldEntity.block(4, 4)
        bot.receive(block)
        world.drop_forward(bot, block)
        assert bot.has(block), 'drop should not happen'

    def test_bot_can_drop_on_empty_space(self):
        world = World(10, 10)
        bot_id = world.add_bot(5, 5, Direction.NORTH)
        bot = world.entity_from_id(bot_id)
        block = WorldEntity.block(4, 4)
        bot.receive(block)
        assert bot.has(block)
        world.drop_forward(bot, block)
        assert not bot.has(block)
        assert world.map.at_xy(5, 4) is block

    def test_bot_cannot_drop_on_used_space(self):
        world = World(10, 10)
        bot_id = world.add_bot(5, 5, Direction.NORTH)
        bot = world.entity_from_id(bot_id)
        blocker_id = world.add_bot(5, 4)
        blocker = world.entity_from_id(blocker_id)
        block = WorldEntity.block(4, 4)
        bot.receive(block)
        assert bot.has(block)
        world.drop_forward(bot, block)
        assert bot.has(block)
        assert world.map.at_xy(5, 4) is blocker

    def test_remove_does_not_forget(self):
        world = World(10, 10)
        block_id = world.add_block(5, 5)
        block = world.entity_from_id(block_id)
        assert world.map.at_xy(5, 5) is block
        world.map.remove(block_id)
        assert world.map.at_xy(5, 5) is None
        assert world.map.at_id(block_id) is block
