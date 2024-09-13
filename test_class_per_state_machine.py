from machine import Looking


class FakeKnowledge():
    def __init__(self, *, can_take=False, has_block=False):
        self.can_take = can_take
        self.has_block = has_block


class TestClassPerStateMachine:
    def test_looking_action_can_take(self):
        state = Looking()
        knowledge = FakeKnowledge(can_take=True)
        assert state.action(knowledge) == ['take']

    def test_looking_action_cannot_take(self):
        state = Looking()
        knowledge = FakeKnowledge(can_take=False)
        assert state.action(knowledge) == []

    def test_looking_update_with_no_block(self):
        state = Looking()
        knowledge = FakeKnowledge(has_block=False)
        machine = None
        n1, n2, looking = state.update(machine, knowledge)
        assert n1 is None
        assert n2 is None
        assert isinstance(looking, Looking)
