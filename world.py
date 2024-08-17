from entities import Entities
from point import Point


class World:
    next_id = 100

    def __init__(self):
        self.entities = Entities()

    def add(self, entity):
        World.next_id += 1
        entity.id = World.next_id
        entity.location = self.find_good_location(entity)
        self.entities.place(entity)

    def find_good_location(self, entity):
        if entity.location:
            return entity.location
        return Point(10, 10)

    def move(self, entity, dx, dy):
        entity = self.entities.contents[entity.id]
        location = entity.location
        entity.location = Point(location.x + dx, location.y + dy)

    def draw(self):
        result = ''
        for y in range(10):
            for x in range(10):
                result += self.location_code(x, y)
            result += '\n'
        return result

    def location_code(self, x, y):
        entity = self.entities.entity_at(x, y)
        if entity:
            return entity.name
        return '_'
