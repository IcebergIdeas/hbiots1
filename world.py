from bot import Bot
from entities import Entities
from point import Point


class World:
    next_id = 100

    def __init__(self, max_x, max_y):
        self.width = max_x
        self.height = max_y
        self.map = Entities()

    def add(self, entity):
        entity.world = self
        World.next_id += 1
        entity.id = World.next_id
        self.map.place(entity)

    def _move(self, entity, dx, dy):
        entity = self.map.contents[entity.id]
        location = entity.location
        new_x = self.clip(location.x + dx, self.width)
        new_y = self.clip(location.y + dy, self.height)
        entity.location = Point(new_x, new_y)
        entity.vision = self.create_vision(entity.location)

    def clip(self, coord, limit):
        return 0 if coord < 0 else (limit if coord > limit else coord)

    def move(self, entity, direction):
        self._move(entity, direction.x, direction.y)

    def create_vision(self, location):
        result = []
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                found = self.map.entity_at(location.x + dx, location.y + dy)
                if found:
                    result.append((found.name, found.x, found.y))
        return result

    def step(self, bot, direction):
        self._move(bot, direction.x, direction.y)

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
        location = bot.location + bot.direction
        entity = self.map.entity_at(location.x, location.y)
        if entity:
            if entity.name != 'R':
                self.map.remove(entity.id)
                bot.receive(entity)

    def drop_forward(self, bot, entity):
        valid_location = self.validate_forward(bot)
        if valid_location != bot.location and self.is_empty(valid_location):
            entity.location = valid_location
            self.add(entity)
            bot.remove(entity)

    def is_empty(self, drop_location):
        return not self.map.entity_at(drop_location.x, drop_location.y)

    def validate_forward(self, bot):
        location = bot.location + bot.direction
        return bot.location if self.is_off_world(location) else location

    def is_off_world(self, location):
        return self.clip(location.x, self.width) != location.x \
            or self.clip(location.y, self.height) != location.y
