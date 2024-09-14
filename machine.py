
class Walking:
    def action(self, _knowledge):
        return []

    def update(self, knowledge):
        if knowledge.tired <= 0:
            if knowledge.has_block:
                return Laden()
            else:
                return Looking()
        return  Walking()


class Looking:
    def update(self, knowledge):
        if knowledge.has_block:
            knowledge.tired = 5
            return Walking()
        else:
            return Looking()

    def action(self, knowledge):
        if knowledge.can_take:
            return ['take']
        return []


class Laden:
    def update(self, knowledge):
        if not knowledge.has_block:
            knowledge.tired = 5
            return Walking()
        else:
            return Laden()

    def action(self, knowledge):
        if knowledge.tired <= 0:
            if knowledge.can_drop:
                return ['drop']
        return []
