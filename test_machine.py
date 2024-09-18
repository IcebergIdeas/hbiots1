from knowledge import Knowledge
from machine import Looking, Laden, Walking


class FakeKnowledge():
    def __init__(self, *,
                 can_take=False,
                 can_drop=False,
                 has_block=False,
                 energy=0):
        self.can_take = can_take
        self.can_drop = can_drop
        self.has_block = has_block
        self._energy = energy

    def has_energy(self):
        return self._energy >= Knowledge.energy_threshold

    def use_energy(self):
        self._energy = 0

    def gain_energy(self):
        self._energy += 1


class TestMachine:
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
        looking = state.update(knowledge)
        assert isinstance(looking, Looking)

    def test_looking_update_with_block(self):
        state = Looking()
        knowledge = FakeKnowledge(has_block=True)
        m_class = state.update(knowledge)
        assert isinstance(m_class, Walking)
        assert knowledge.has_energy() is False

    def test_laden_action_tired_cannot_drop(self):
        state = Laden()
        knowledge = FakeKnowledge(can_drop=True)
        assert state.action(knowledge) == []

    def test_laden_action_not_tired_cannot_drop(self):
        state = Laden()
        knowledge = FakeKnowledge(energy=0, can_drop=False)
        assert state.action(knowledge) == []

    def test_laden_action_not_tired_can_drop(self):
        state = Laden()
        knowledge = FakeKnowledge(energy=Knowledge.energy_threshold, can_drop=True)
        assert state.action(knowledge) == ['drop']

    def test_laden_update_has_block(self):
        state = Laden()
        knowledge = FakeKnowledge(has_block=True)
        c = state.update(knowledge)
        assert isinstance(c, Laden)

    def test_laden_update_has_no_block(self):
        state = Laden()
        knowledge = FakeKnowledge(has_block=False)
        m_class = state.update(knowledge)
        assert isinstance(m_class, Walking)
        assert not knowledge.has_energy()

    def test_walking_action_returns_empty_list(self):
        state = Walking()
        knowledge = FakeKnowledge()
        assert state.action(knowledge) == []

    def test_walking_tired_without_block_keeps_walking(self):
        state = Walking()
        knowledge = FakeKnowledge(energy=0, has_block=False)
        c = state.update(knowledge)
        assert isinstance(c, Walking)

    def test_walking_tired_with_block_keeps_walking(self):
        state = Walking()
        knowledge = FakeKnowledge(energy=0, has_block=True)
        c = state.update(knowledge)
        assert isinstance(c, Walking)

    def test_walking_not_tired_with_block_goes_laden(self):
        state = Walking()
        knowledge = FakeKnowledge(energy=Knowledge.energy_threshold, has_block=True)
        c = state.update(knowledge)
        assert isinstance(c, Laden)

    def test_walking_not_tired_without_block_goes_looking(self):
        state = Walking()
        knowledge = FakeKnowledge(energy=Knowledge.energy_threshold, has_block=False)
        c = state.update(knowledge)
        assert isinstance(c, Looking)


