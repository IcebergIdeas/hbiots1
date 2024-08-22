from block import Block
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

    def clip(self, coord, limit):
        if coord < 0:
            return 0
        if coord > limit:
            return limit
        return coord

    def move_north(self, entity):
        self._move(entity, 0, 1)

    def move_east(self, entity):
        self._move(entity, 1, 0)

    def move_south(self, entity):
        self._move(entity, 0, -1)

    def move_west(self, entity):
        self._move(entity, -1, 0)

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

    def take_east(self, bot: Bot):
        location = bot.location + Point(1, 0)
        entity = self.map.entity_at(location.x, location.y)
        if entity:
            self.map.remove(entity.id)
            bot.receive(entity)

    def drop_north(self, bot):
        block = Block(bot.x, bot.y + 1)
        self.add(block)

    def drop_west(self, bot):
        block = Block(bot.x - 1, bot.y)
        self.add(block)

    def drop_south(self, bot):
        block = Block(bot.x, bot.y - 1)
        self.add(block)
