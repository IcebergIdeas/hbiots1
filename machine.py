
class Machine:
    def __init__(self, bot):
        self.bot = bot
        self.vision = bot.vision
        self.tired = 10
        self._update = self.update_walking
        self._action = self.walking

    def state(self, bot):
        self.bot = bot
        self.vision = bot.vision
        self.tired -= 1
        self._update()
        self._action()
        return self

    def update_laden(self):
        pass

    def update_walking(self):
        if self.tired <= 0:
            if self.bot.inventory:
                self._update = self.update_laden
                self._action = self.laden
            else:
                self._update = self.update_looking
                self._action = self.looking

    def walking(self):
        pass

    def update_looking(self):
        if self.bot.inventory:
            self.tired = 5
            self._update = self.update_walking
            self._action = self.walking

    def looking(self):
        if self.bot.can_take():
            self.bot.take()

    def laden(self):
        if self.bot.has_no_block():
            self.tired = 5
            self._update = self.update_walking
            self._action = self.walking
            return
        if self.tired <= 0:
            if self.bot.can_drop():
                block = self.bot.inventory[0]
                self.bot.drop(block)
