from map_entity import MapEntity
from location import Location


class Map:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.contents = {}

    def __iter__(self):
        return iter(self.contents.values())

    def place(self, entity):
        self.contents[entity.id] = entity

    def entity_at(self, x, y):
        point = Location(x, y)
        for entity in self.contents.values():
            if entity.location == point:
                return entity
        return None

    def map_is_OK(self, other: [MapEntity]):
        other_entities = other.get_entities()
        if not self.check_all_other_entities_are_valid(other_entities):
            return False
        return len(self.contents) == len(other_entities)

    def check_all_other_entities_are_valid(self, other_contents: [MapEntity]):
        other_entities_are_all_valid = True
        for map_entity in other_contents:
            if self.entity_at(map_entity.x, map_entity.y).name != map_entity.name:
                other_entities_are_all_valid = False
        return other_entities_are_all_valid

    def remove(self, id):
        del self.contents[id]

    def attempt_move(self, id, location: Location):
        entity = self.contents[id]
        if self.location_is_valid(location):
            entity.location = location

    def location_is_valid(self, location: Location) -> bool:
        if self.is_occupied(location):
            return False
        return self.is_within_map(location)

    def is_within_map(self, location):
        return 0 <= location.x <= self.width and 0 <= location.y <= self.height

    def is_occupied(self, location):
        return self.entity_at(location.x, location.y)

    def create_vision(self, location):
        result = []
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                found = self.entity_at(location.x + dx, location.y + dy)
                if found:
                    result.append((found.name, found.x, found.y))
        return result
