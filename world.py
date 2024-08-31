from bot import Bot
from map import Map
from location import Location


class World:
    next_id = 100

    def __init__(self, max_x, max_y):
        self.width = max_x
        self.height = max_y
        self.map = Map(10, 10)

    def add(self, entity):
        entity.world = self
        World.next_id += 1
        entity.id = World.next_id
        self.map.place(entity)

    def _move(self, entity):
        entity = self.map.contents[entity.id]
        entity.location = self.bots_next_location(entity)
        entity.vision = self.create_vision(entity.location)

    def step(self, bot):
        self._move(bot)

    def clip(self, coord, limit):
        return 0 if coord < 0 else (limit if coord > limit else coord)

    def create_vision(self, location):
        result = []
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                found = self.map.entity_at(location.x + dx, location.y + dy)
                if found:
                    result.append((found.name, found.x, found.y))
        return result

    def draw(self):
        result = ''
        for y in range(10):
            for x in range(10):
                result += self._location_code(x, y)
            result += '\n'
        return result

    def _location_code(self, x, y):
        entity = self.map.entity_at(x, y)
        if entity:
            return entity.name
        return '_'

    def scan(self, bot):
        return [(e.name, e.x, e.y) for e in self.map if e.is_close_enough(bot)]

    def take_forward(self, bot: Bot):
        take_location = self.bots_next_location(bot)
        if take_location == bot.location:
            return
        entity = self.map.entity_at(take_location.x, take_location.y)
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
        return not self.map.entity_at(drop_location.x, drop_location.y)

    def bots_next_location(self, bot):
        location = bot.location + bot.direction
        return bot.location if self.is_off_world(location) else location

    def is_off_world(self, location):
        return self.clip(location.x, self.width) != location.x \
            or self.clip(location.y, self.height) != location.y
