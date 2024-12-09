
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
            case {'bot_key': bot_key, 'verb': verb}:
                assert bot_key == 101
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
            case { 'bot_key': bot_key, 'verb': 'take'}:
                assert False  # not here
            case { 'bot_key': bot_key, 'verb': verb}:
                assert bot_key == 101
                assert verb == 'add_bot'
            case _:
                assert False  # should match above

    def test_plug_in_entity_object(self):
        # just a test of how we might do things
        def entity_from_key(key):
            return f'entity_object_{key}'
        d = {'bot_key': 0, 'verb': 'add_bot'}
        self.check_cases(d, entity_from_key)
        d = {'bot_key': 101, 'verb': 'take'}
        self.check_cases(d, entity_from_key)

    def check_cases(self, d, lookup):
        match d:
            case {'bot_key': 0}:
                d['entity'] = None
            case {'bot_key': bot_key}:
                d['entity'] = lookup(bot_key)
        match d:
            case {'entity': None, 'verb': 'add_bot'}:
                pass
            case {'entity': obj, 'verb': verb}:
                assert verb == 'take'
                assert obj == 'entity_object_101'
            case _:
                assert False

    def test_interpolation(self):
        s = 'message {verb} does not like {direction}'
        s_i = s.format(verb = 'turn', direction = 'RIGHT')
        assert s_i == 'message turn does not like RIGHT'

