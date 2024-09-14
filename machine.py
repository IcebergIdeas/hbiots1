from knowledge import Knowledge


class Walking:
    def action(self, _knowledge):
        return []

    def update(self, machine, knowledge):
        return None, None, Walking()


class Looking:
    def update(self, machine, knowledge):
        if knowledge.has_block:
            knowledge.tired = 5
            return machine.walking_update, machine.walking_action, None
        else:
            return None, None, Looking()

    def action(self, knowledge):
        if knowledge.can_take:
            return ['take']
        return []


class Laden:
    def update(self, machine, knowledge):
        if not knowledge.has_block:
            knowledge.tired = 5
            return machine.walking_update, machine.walking_action, None
        else:
            return None, None, Laden()

    def action(self, knowledge):
        if knowledge.tired <= 0:
            if knowledge.can_drop:
                return ['drop']
        return []


class Machine:
    def __init__(self, knowledge):
        assert isinstance(knowledge, Knowledge)
        self._knowledge = knowledge
        self._update = self.walking_update
        self._action = self.walking_action
        self._state = None

    def state(self, knowledge):
        assert isinstance(knowledge, Knowledge)
        self._knowledge = knowledge
        knowledge.tired -= 1
        if self._state:
            info = self._state.update(self, self._knowledge)
            self._update, self._action, self._state = info
        else:
            info = self._update()
            self._update, self._action, self._state = info
        if self._state:
            return self._state.action(self._knowledge)
        else:
            return self._action()

    def walking_states(self):
        return self.walking_update, self.walking_action, None

    def looking_states(self):
        return None, None, Looking()

    def laden_states(self):
        return self.laden_update, self.laden_action, None

    def set_states(self, states):
        self._update, self._action, self._state = states

    def walking_update(self):
        if self._knowledge.tired <= 0:
            if self._knowledge.has_block:
                return None, None, Laden()
            else:
                return None, None, Looking()
        return self.walking_states()

    def walking_action(self):
        return []

    def looking_update(self):
        if self._knowledge.has_block:
            self._knowledge.tired = 5
            return self.walking_states()
        else:
            return self.looking_states()

    def looking_action(self):
        if self._knowledge.can_take:
            return ['take']
        return []

    def laden_update(self):
        if not self._knowledge.has_block:
            self._knowledge.tired = 5
            return self.walking_states()
        else:
            return self.laden_states()

    def laden_action(self):
        if self._knowledge.tired <= 0:
            if self._knowledge.can_drop:
                return ['drop']
        return []
