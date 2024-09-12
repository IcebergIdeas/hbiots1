from knowledge import Knowledge


class Machine:
    def __init__(self, knowledge):
        assert isinstance(knowledge, Knowledge)
        self._knowledge = knowledge
        self.tired = 10
        self._update = self.walking_update
        self._action = self.walking_action
        self._state = None

    def state(self, knowledge):
        assert isinstance(knowledge, Knowledge)
        self._knowledge = knowledge
        self.tired -= 1
        if self._state:
            self._state.update()
        else:
            info = self._update()
            self._update, self._action, self._state = info
        if self._state:
            self._state.action()
        else:
            return self._action()

    def walking_states(self):
        return self.walking_update, self.walking_action, None

    def looking_states(self):
        return self.looking_update, self.looking_action, None

    def laden_states(self):
        return self.laden_update, self.laden_action, None

    def set_states(self, states):
        self._update, self._action, self._state = states

    def walking_update(self):
        if self.tired <= 0:
            if self._knowledge.has_block:
                return self.laden_states()
            else:
                return self.looking_states()
        return self.walking_states()

    def walking_action(self):
        return []

    def looking_update(self):
        if self._knowledge.has_block:
            self.tired = 5
            return self.walking_states()
        else:
            return self.looking_states()

    def looking_action(self):
        if self._knowledge.can_take:
            return ['take']
        return []

    def laden_update(self):
        if not self._knowledge.has_block:
            self.tired = 5
            return self.walking_states()
        else:
            return self.laden_states()

    def laden_action(self):
        if self.tired <= 0:
            if self._knowledge.can_drop:
                return ['drop']
        return []
