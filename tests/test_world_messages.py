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
        requests = { 'bot_key': 0, 'verb': 'add_bot'}
        messages = world.execute_requests(requests)['messages']
        assert any('must be a list' in message['message'] for message in messages)

    def test_no_verb(self):
        world = World(10, 10)
        requests = [{'entity_object': "fake", 'vorb': 'add_bot'}]
        messages = world.execute_requests(requests)['messages']
        assert 'Unknown action' in messages[0]['message']

    def test_bad_verb(self):
        world = World(10, 10)
        requests = [{'entity_object': "fake", 'verb': 'whatever'}]
        messages = world.execute_requests(requests)['messages']
        assert "Unknown action verb='whatever'" in messages[0]['message']

    def test_no_entity(self):
        world = World(10, 10)
        requests = [ {'verb': 'step'}]
        messages = world.execute_requests(requests)['messages']
        assert 'requires entity parameter' in messages[0]['message']

    def test_action_must_be_dict(self):
        world = World(10, 10)
        requests = [ {'verb', 'step'}]
        messages = world.execute_requests(requests)['messages']
        assert 'must be dictionary' in messages[0]['message']

    def test_invalid_turn_message(self):
        world = World(10, 10)
        bot_id = world.add_bot(5, 5)
        requests = [{'bot_key': bot_id, 'verb': 'turn', 'direction': 'LEFT'}]
        messages = world.execute_requests(requests)['messages']
        expected = 'unknown direction LEFT, should be NORTH, EAST, SOUTH, or WEST'
        assert expected in messages[0]['message']

    def test_add_bot_bad_direction(self):
        world = World(10, 10)
        requests = [ {'verb': 'add_bot',
                      'bot_key': 0,
                      'x': 5, 'y': 5,
                      'direction': 'WRONG'}]
        messages = world.execute_requests(requests)['messages']
        expected = 'add_bot has unknown direction WRONG, should be NORTH, EAST, SOUTH, or WEST'
        assert messages[0]['message'] == expected


