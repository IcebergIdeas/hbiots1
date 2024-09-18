
class Walking:
    def action(self, _knowledge):
        return []

    def update(self, knowledge):
        if knowledge.has_energy():
            if knowledge.has_block:
                return Laden()
            else:
                return Looking()
        return Walking()


class Looking:
    def action(self, knowledge):
        if knowledge.can_take:
            return ['take']
        return []

    def update(self, knowledge):
        if knowledge.has_block:
            knowledge.use_energy()
            return Walking()
        else:
            return Looking()



class Laden:
    def action(self, knowledge):
        if knowledge.has_energy():
            if knowledge.can_drop:
                return ['drop']
        return []

    def update(self, knowledge):
        if not knowledge.has_block:
            knowledge.use_energy()
            return Walking()
        else:
            return Laden()

