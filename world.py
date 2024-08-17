from entities import Entities
from point import Point


class World:
    next_id = 100

    def __init__(self):
        self.biots = Entities()

    def add(self, biot):
        location = Point(10, 10)
        World.next_id += 1
        biot.id = World.next_id
        biot.location = location
        self.biots.place(biot)

    def move(self, biot, dx, dy):
        biot = self.biots.contents[biot.id]
        location = biot.location
        biot.location = Point(location.x + dx, location.y + dy)

    def draw(self):
        result = ''
        for y in range(10):
            for x in range(10):
                result += self.location_code(x, y)
            result += '\n'
        return result

    def location_code(self, x, y):
        entity = self.biots.entity_at(x, y)
        if entity:
            return entity.name
        return '_'
