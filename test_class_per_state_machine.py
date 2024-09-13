from machine import Looking


class FakeKnowledge():
    def __init__(self, *, can_take=False):
        self.can_take = can_take


class TestClassPerStateMachine:
    def test_looking_action_can_take(self):
        state = Looking()
        knowledge = FakeKnowledge(can_take=True)
        assert state.action(knowledge) == ['take']

    def test_looking_action_cannot_take(self):
        state = Looking()
        knowledge = FakeKnowledge(can_take=False)
        assert state.action(knowledge) == []
