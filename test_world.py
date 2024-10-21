from direction import Direction
from location import Location
from world import World


def test_take_a_block():
    world = World(10, 10)
    bot_id = world.add_bot(5, 5)
    world.add_block(6, 5)
    assert not world.is_empty(Location(6, 5))
    bot = world.entity_from_id(bot_id)
    world.take_forward(bot)
    assert bot.has_block()
    assert world.is_empty(Location(6, 5))

def test_bot_facing_north_takes_a_north_block():
    check_directional_take((5, 5), (5, 4), Direction.NORTH)

def test_bot_facing_east_takes_an_east_block():
    check_directional_take((5, 5), (6,5), Direction.EAST)

def test_bot_facing_south_takes_a_south_block():
    check_directional_take((5, 5), (5, 6), Direction.SOUTH)

def test_bot_facing_west_takes_a_west_block():
    check_directional_take((5, 5), (4, 5), Direction.WEST)

def check_directional_take(bot_loc, block_loc, direction):
    bot_x, bot_y = bot_loc
    block_x, block_y = block_loc
    world = World(10, 10)
    bot_id = world.add_bot(bot_x, bot_y, direction)
    bot = world.entity_from_id(bot_id)
    world.add_block(block_x, block_y)
    world.take_forward(bot)
    assert bot.has_block()