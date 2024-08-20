from entities import Entities
from point import Point


class World:
    next_id = 100

    def __init__(self):
        self.map = Entities()

    def add(self, entity):
        entity.world = self
        World.next_id += 1
        entity.id = World.next_id
        entity.location = self._find_good_location(entity)
        self.map.place(entity)

    def _find_good_location(self, entity):
        if entity.location:
            return entity.location
        return Point(10, 10)

    def _move(self, entity, dx, dy):
        entity = self.map.contents[entity.id]
        location = entity.location
        entity.location = Point(location.x + dx, location.y + dy)

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
