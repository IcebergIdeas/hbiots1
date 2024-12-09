
class TestPython:
    def test_hook(self):
        assert True

    def test_dictionary_unpack(self):
        def func(b, **kw):
            assert b == 2
        d = {'a': 1, 'b': 2, 'c': 3}
        func(**d)

    def test_match_case_dict(self):
        d = {'bot_key': 101, 'verb': 'take'}
        match d:
            case {'bot_key': entity_id, 'verb': verb}:
                assert entity_id == 101
                assert verb == 'take'
            case _:
                assert False  # should never get here

    def test_match_case_literal(self):
        d = {'bot_key': 0, 'verb': 'add_bot'}
        match d:
            case {'bot_key': 0, 'verb': 'add_bot'}:
                pass
            case _:
                assert False  # should never get here

    def test_match_case_literal_unmatched(self):
        d = {'bot_key': 101, 'verb': 'add_bot'}
        match d:
            case {'bot_key': 0, 'verb': 'add_bot'}:
                assert False  # should not match
            case { 'bot_key': entity_id, 'verb': 'take'}:
                assert False  # not here
            case { 'bot_key': entity_id, 'verb': verb}:
                assert entity_id == 101
                assert verb == 'add_bot'
            case _:
                assert False  # should match above

    def test_plug_in_entity_object(self):
        def entity_from_id(entity_id):
            return f'entity_object_{entity_id}'
        d = {'bot_key': 0, 'verb': 'add_bot'}
        self.check_cases(d, entity_from_id)
        d = {'bot_key': 101, 'verb': 'take'}
        self.check_cases(d, entity_from_id)

    def check_cases(self, d, entity_from_id):
        match d:
            case {'bot_key': 0}:
                d['entity_object'] = None
            case {'bot_key': entity_id}:
                d['entity_object'] = entity_from_id(entity_id)
        match d:
            case {'entity_object': None, 'verb': 'add_bot'}:
                pass
            case {'entity_object': obj, 'verb': verb}:
                assert verb == 'take'
                assert obj == 'entity_object_101'
            case _:
                assert False

