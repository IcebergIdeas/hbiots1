from machine import Looking, Laden


class FakeKnowledge():
    def __init__(self, *,
                 can_take=False,
                 can_drop=False,
                 has_block=False,
                 tired=99):
        self.can_take = can_take
        self.can_drop = can_drop
        self.has_block = has_block
        self.tired = tired


class FakeMachine:
    def walking_update(self):
        pass

    def walking_action(self):
        pass


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

    def test_looking_update_with_block(self):
        state = Looking()
        knowledge = FakeKnowledge(has_block=True)
        machine = FakeMachine()
        m_update, m_action, m_class = state.update(machine, knowledge)
        assert m_update == machine.walking_update
        assert m_action == machine.walking_action
        assert m_class is None
        assert knowledge.tired == 5

    def test_laden_action_tired_cannot_drop(self):
        state = Laden()
        knowledge = FakeKnowledge(tired=99, can_drop=True)
        assert state.action(knowledge) == []

    def test_laden_action_not_tired_cannot_drop(self):
        state = Laden()
        knowledge = FakeKnowledge(tired=0, can_drop=False)
        assert state.action(knowledge) == []

    def test_laden_action_not_tired_can_drop(self):
        state = Laden()
        knowledge = FakeKnowledge(tired=0, can_drop=True)
        assert state.action(knowledge) == ['drop']

    def test_laden_update_has_block(self):
        state = Laden()
        knowledge = FakeKnowledge(has_block=True)
        u, a, c = state.update(None, knowledge)
        assert u is None
        assert a is None
        assert isinstance(c, Laden)
