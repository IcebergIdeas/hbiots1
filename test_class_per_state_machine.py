from machine import Looking


class FakeKnowledge():
    def __init__(self, *, can_take=False):
        self.can_take = can_take


class TestClassPerStateMachine:
    def test_looking_action(self):
        state = Looking()
        knowledge = FakeKnowledge(can_take=True)
        assert state.action(knowledge) == ['take']
