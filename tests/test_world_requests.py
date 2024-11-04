

class TestWorldRequests:
    def test_hookup(self):
        assert True

    def test_imaginary_request(self):
        single_request = {
            "entity": 100,
            "actions": [
                {"verb": "take"},
                {"verb": 'step'}
            ]
        }
        id = single_request['entity']
        assert id == 100
        first_action = single_request['actions'][0]
        assert first_action['verb'] == 'take'