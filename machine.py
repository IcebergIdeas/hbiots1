
class Machine:
    def __init__(self, bot):
        self.bot = bot
        self.vision = bot.vision
        self.tired = 10
        self._update = self.walking_update
        self._action = self.walking_action

    def state(self, bot):
        self.bot = bot
        self.vision = bot.vision
        self.tired -= 1
        self._update()
        self._action()
        return self

    def walking_update(self):
        if self.tired <= 0:
            if self.bot.inventory:
                self._update = self.laden_update
                self._action = self.laden_action
            else:
                self._update = self.looking_update
                self._action = self.looking_action

    def walking_action(self):
        pass

    def looking_update(self):
        if self.bot.inventory:
            self.tired = 5
            self._update = self.walking_update
            self._action = self.walking_action

    def looking_action(self):
        if self.bot.can_take():
            self.bot.take()

    def laden_update(self):
        if self.bot.has_no_block():
            self.tired = 5
            self._update = self.walking_update
            self._action = self.walking_action

    def laden_action(self):
        if self.tired <= 0:
            if self.bot.can_drop():
                block = self.bot.inventory[0]
                self.bot.drop(block)
