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