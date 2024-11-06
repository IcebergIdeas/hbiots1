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
