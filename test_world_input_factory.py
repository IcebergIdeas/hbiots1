from world import World


class InputBuilder:
    def __init__(self, world):
        from test_world_batch import WorldInput
        self._world = world
        self._world_input = WorldInput()
        self._current_request = None

    def request(self, identifier):
        from test_world_batch import EntityRequest
        self._current_request = EntityRequest(identifier, self._world)
        self._world_input.add_request(self._current_request)
        return self

    def action(self, action_word, parameter=None):
        from test_world_batch import EntityAction
        operation = EntityAction(action_word, parameter)
        self._current_request.add_action(operation)
        return self

    def result(self):
        return self._world_input

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
