from direction import Direction
from location import Location
from world import World


class TestVision:
    def test_hookup(self):
        assert True

    def test_nothing_near(self):
        world = World(10, 10)
        bot = world.add_bot(5, 5)
        bot.direction_change_chance = 0.0
        bot.vision = None
        bot.move()
        assert bot.location == Location(6, 5)
        vision = bot.vision
        assert ('R', 6, 5) in vision

    def test_three_blocks_near(self):
        from block import Block
        world = World(10, 10)
        world.add(Block(4, 4))
        world.add(Block(6, 6))
        world.add(Block(4, 5))
        bot = world.add_bot(6, 5)
        bot.direction = Direction.WEST
        bot.direction_change_chance = 0.0
        bot.vision = None
        bot.move()
        assert bot.location == Location(5, 5)
        vision = bot.vision
        assert ('R', 5, 5) in vision
        assert ('B', 4, 5) in vision
        assert ('B', 6, 6) in vision
        assert ('B', 4, 4) in vision
