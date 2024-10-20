import pytest

from new_knowledge import NewKnowledge


class TestDictionaryIdea:
    def test_dict_with_dot_access(self):
        knowledge = NewKnowledge()
        knowledge.id = 100
        assert knowledge._dict["id"] == 100
        assert knowledge.id == 100
        knowledge._scent = 31
        assert knowledge._dict["_scent"] == 31
        assert knowledge._scent == 31
        with pytest.raises(KeyError):
            _ = knowledge.unknown
        with pytest.raises(AttributeError):
            knowledge.unknown = 15