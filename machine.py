
class Machine:
    def __init__(self, knowledge):
        self._knowledge = knowledge
        self.tired = 10
        self._update = self.walking_update
        self._action = self.walking_action

    def state(self, knowledge):
        self._knowledge = knowledge
        self.tired -= 1
        self._update()
        self._action()
        return self

    def walking_states(self):
        return self.walking_update, self.walking_action

    def looking_states(self):
        return self.looking_update, self.looking_action

    def laden_states(self):
        return self.laden_update, self.laden_action

    def set_states(self, states):
        self._update, self._action = states

    def walking_update(self):
        if self.tired <= 0:
            if self._knowledge.inventory:
                self.set_states(self.laden_states())
            else:
                self.set_states(self.looking_states())

    def walking_action(self):
        pass

    def looking_update(self):
        if self._knowledge.inventory:
            self.tired = 5
            self.set_states(self.walking_states())

    def looking_action(self):
        if self._knowledge.can_take():
            self._knowledge.take()

    def laden_update(self):
        if self._knowledge.has_no_block():
            self.tired = 5
            self.set_states(self.walking_states())

    def laden_action(self):
        if self.tired <= 0:
            if self._knowledge.can_drop():
                block = self._knowledge.inventory[0]
                self._knowledge.drop(block)
