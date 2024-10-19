import pytest


class NewKnowledge:
    def __init__(self):
        self._dict = dict()

    def __getattr__(self, item):
        return self._dict[item]

    def __setattr__(self, key, value):
        known = ['id', 'scent']
        if key == '_dict':
            return super().__setattr__(key, value)
        if key in known:
            self._dict[key] = value
        else:
            raise AttributeError(f'{key} not in {known}')


class TestDictionaryIdea:
    def test_dict_with_dot_access(self):
        knowledge = NewKnowledge()
        knowledge.id = 100
        assert knowledge._dict["id"] == 100
        assert knowledge.id == 100
        knowledge.scent = 31
        assert knowledge._dict["scent"] == 31
        assert knowledge.scent == 31
        with pytest.raises(KeyError):
            _ = knowledge.unknown
        with pytest.raises(AttributeError):
            knowledge.unknown = 15