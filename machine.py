
class Machine:
    def __init__(self, bot):
        self.bot = bot
        self.vision = bot.vision
        self.tired = 10
        self._action = self.walking

    def state(self, bot):
        self.bot = bot
        self.vision = bot.vision
        self.tired -= 1
        self._action()
        return self

    def walking(self):
        if self.tired <= 0:
            self._action = self.laden if self.bot.inventory else self.looking

    def looking(self):
        if self.bot.inventory:
            self.tired = 5
            self._action = self.walking
            return
        if self.bot.can_take():
            self.bot.take()

    def laden(self):
        if self.bot.has_no_block():
            self.tired = 5
            self._action = self.walking
            return
        if self.tired <= 0:
            if self.bot.can_drop():
                block = self.bot.inventory[0]
                self.bot.drop(block)