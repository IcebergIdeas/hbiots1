from server.world import World


class TestWorldMessages:
    def test_list_exists(self):
        world = World(10, 10)
        requests = []
        result = world.execute_requests(requests)
        assert result['messages'] == []
        assert result['updates'] == []

    def test_requests_must_be_list(self):
        world = World(10, 10)
        requests = { 'entity': 0, 'verb': 'add_bot'}
        messages = world.execute_requests(requests)['messages']
        assert any('must be a list' in message['message'] for message in messages)

