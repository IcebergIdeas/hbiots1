from location import Location
from world import World


class TestVision:
    def test_hookup(self):
        assert True

    def test_nothing_near(self):
        world = World(10, 10)
        client_bot = world.add_bot(5, 5)
        real_bot = world.map.at_id(client_bot.id)
        client_bot.direction_change_chance = 0.0
        real_bot.direction_change_chance = 0.0
        client_bot.vision = []
        client_bot.do_something()
        world.update_client_for_test(client_bot)
        assert client_bot.location == Location(6, 5)
        vision = client_bot.vision
        assert ('R', 6, 5) in vision

    def test_three_blocks_near(self):
        from block import Block

        def turn_move_and_update():
            client_bot.perform_actions(['WEST', 'step'])
            world.update_client_for_test(client_bot)
            actions = client_bot.update_for_state_machine()
            client_bot.perform_actions(actions)

        world = World(10, 10)
        world.add(Block(4, 4))
        world.add(Block(6, 6))
        world.add(Block(4, 5))
        client_bot = world.add_bot(6, 5)
        client_bot.direction_change_chance = 0.0
        client_bot.vision = None
        turn_move_and_update()
        assert client_bot.location == Location(5, 5)
        vision = client_bot.vision
        assert ('R', 5, 5) in vision
        assert ('B', 4, 5) in vision
        assert ('B', 6, 6) in vision
        assert ('B', 4, 4) in vision
