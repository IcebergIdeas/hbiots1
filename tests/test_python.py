
class TestPython:
    def test_hook(self):
        assert True

    def test_dictionary_unpack(self):
        def func(b, **kw):
            assert b == 2
        d = {'a': 1, 'b': 2, 'c': 3}
        func(**d)