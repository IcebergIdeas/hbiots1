from server.input_builder import InputBuilder
from server.world import World


class TestWorldInputFactory:
    def test_building(self):
        world = World(5,5)
        bot_id = world.add_bot(5, 5)
        block_id = world.add_block(7,8)
        world_input = InputBuilder(world) \
            .request(bot_id) \
                .action('take') \
                .action('turn','SOUTH') \
                .action('step') \
                .action('step') \
                .action('drop', block_id) \
            .request(world.add_bot(7, 7)) \
                .action('step') \
                .action('step') \
            .result()
        assert len(world_input._requests) == 2
