from server.world import World
from shared.direct_connection import DirectConnection
from shared.location import Location


class TestVision:
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
