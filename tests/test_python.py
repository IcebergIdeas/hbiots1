
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
        d = { 'x': 10, 'direction': 'EAST'}
        s = 'message {verb} does not like {direction}'
        s1 = s.format(verb = 'turn', direction = 'RIGHT')
        assert s1 == 'message turn does not like RIGHT'
        s2 = s.format(verb = 'turn', direction = d)
        assert s2 == "message turn does not like {'x': 10, 'direction': 'EAST'}"

    def test_varargs(self):
        s = 'message {verb} does not like {direction}'
        def message(msg_name, **kwargs):
            prototype = s if msg_name == 's' else None
            return prototype.format(**kwargs)

        d = { 'x': 10, 'direction': 'EAST'}
        m = message('s', verb = 'turn', direction = d, unexpected = "boo!")
        assert m == "message turn does not like {'x': 10, 'direction': 'EAST'}"
