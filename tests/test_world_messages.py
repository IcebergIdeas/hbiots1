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

    def test_no_verb(self):
        world = World(10, 10)
        requests = [{'entity_object': "fake", 'vorb': 'add_bot'}]
        messages = world.execute_requests(requests)['messages']
        assert 'Unknown action' in messages[0]['message']

    def test_no_entity(self):
        world = World(10, 10)
        requests = [ {'verb': 'step'}]
        messages = world.execute_requests(requests)['messages']
        assert 'requires entity parameter' in messages[0]['message']