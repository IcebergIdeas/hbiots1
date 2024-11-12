from server.world import World
from shared.direct_connection import DirectConnection
from shared.location import Location


class TestVision:
    def test_hookup(self):
        assert True

    def test_nothing_near(self):
        world = World(10, 10)
        client_bot = DirectConnection(world).add_bot(5, 5)
        real_bot = world.map.at_id(client_bot.id)
        client_bot.direction_change_chance = 0.0
        real_bot.direction_change_chance = 0.0
        client_bot.vision = []
        client_bot.do_something_only_for_tests(DirectConnection(world))
        world.update_client_for_test(client_bot)
        assert client_bot.location == Location(6, 5)
        vision = client_bot.vision
        assert ('R', 6, 5) in vision

    def test_three_blocks_near(self):
        world = World(10, 10)
        world.add_block(4, 4)
        world.add_block(6, 6)
        world.add_block(4, 5)
        DirectConnection(world).add_bot(5, 5)
        vision = world.map.vision_at(Location(5, 5))
        assert ('R', 5, 5) in vision
        assert ('B', 4, 5) in vision
        assert ('B', 6, 6) in vision
        assert ('B', 4, 4) in vision
