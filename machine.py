class Walking:
    def action(self, _knowledge):
        return []

    def update(self, machine, knowledge):
        if knowledge.tired <= 0:
            if knowledge.has_block:
                return None, None, Laden()
            else:
                return None, None, Looking()
        return None, None, Walking()


class Looking:
    def update(self, machine, knowledge):
        if knowledge.has_block:
            knowledge.tired = 5
            return None, None, Walking()
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
            return None, None, Walking()
        else:
            return None, None, Laden()

    def action(self, knowledge):
        if knowledge.tired <= 0:
            if knowledge.can_drop:
                return ['drop']
        return []


class Machine:
    def __init__(self, knowledge):
        self._knowledge = knowledge
        self._state = Walking()

    def state(self, knowledge):
        self._knowledge = knowledge
        knowledge.tired -= 1
        info = self._state.update(self, self._knowledge)
        self.set_states(info)
        return self._state.action(self._knowledge)

    def set_states(self, states):
        _, _, self._state = states

