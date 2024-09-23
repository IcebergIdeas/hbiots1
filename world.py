from bot import Bot
from map import Map


class World:
    next_id = 100

    def __init__(self, max_x, max_y):
        self.width = max_x
        self.height = max_y
        self.map = Map(max_x, max_y)

    def add(self, entity):
        entity.world = self
        World.next_id += 1
        entity.id = World.next_id
        self.map.place(entity)

    def command(self, action, parameter):
        if action == 'step':
            bot = self.map.at_id(parameter)
            self.step(bot)
        else:
            raise Exception('Unknown command')

    def fetch(self, entity_id):
        return self.map.at_id(entity_id)._knowledge

    def step(self, bot):
        location = self.bots_next_location(bot)
        self.map.attempt_move(bot.id, location)
        self.set_bot_vision(bot)
        self.set_bot_scent(bot)

    def set_bot_vision(self, bot):
        bot.vision = self.map.vision_at(bot.location)

    def set_bot_scent(self, bot):
        bot.scent = self.map.scent_at(bot.location)

    def clip(self, coord, limit):
        return 0 if coord < 0 else (limit if coord > limit else coord)

    def draw(self):
        result = ''
        for y in range(10):
            for x in range(10):
                result += self._location_code(x, y)
            result += '\n'
        return result

    def _location_code(self, x, y):
        entity = self.map.at_xy(x, y)
        if entity:
            return entity.name
        return '_'

    def take_forward(self, bot: Bot):
        take_location = self.bots_next_location(bot)
        if take_location == bot.location:
            return
        entity = self.map.at_xy(take_location.x, take_location.y)
        if self.can_take_entity(entity):
            self.map.remove(entity.id)
            bot.receive(entity)

    def can_take_entity(self, entity):
        return entity and entity.name != 'R'

    def drop_forward(self, bot, entity):
        drop_location = self.bots_next_location(bot)
        if drop_location != bot.location and self.is_empty(drop_location):
            entity.location = drop_location
            self.add(entity)
            bot.remove(entity)

    def is_empty(self, drop_location):
        return not self.map.at_xy(drop_location.x, drop_location.y)

    def bots_next_location(self, bot):
        location = bot.location + bot.direction
        return bot.location if self.is_off_world(location) else location

    def is_off_world(self, location):
        return self.clip(location.x, self.width) != location.x \
            or self.clip(location.y, self.height) != location.y
