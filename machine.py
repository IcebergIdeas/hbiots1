
class Machine:
    def __init__(self, bot):
        self.bot = bot
        self.tired = 10
        self._state = self.walking

    def state(self):
        self.tired -= 1
        self._state()
        return self

    def walking(self):
        if self.tired <= 0:
            self._state = self.laden if self.bot.inventory else self.looking

    def looking(self):
        if self.bot.inventory:
            self.tired = 5
            self._state = self.walking
            return
        if self.bot.can_take():
            self.bot.take()

    def laden(self):
        if self.bot.has_no_block():
            self.tired = 5
            self._state = self.walking
            return
        if self.tired <= 0:
            if self.bot.can_drop():
                block = self.bot.inventory[0]
                self.bot.drop(block)
