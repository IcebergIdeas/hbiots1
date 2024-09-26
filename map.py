from direction import Direction
from location import Location
from map_entity import MapEntity


class Map:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.contents = {}

    def __iter__(self):
        return iter(self.contents.values())

    def at_id(self, entity_id):
        return self.contents[entity_id]

    def at_xy(self, x, y):
        point = Location(x, y)
        for entity in self.contents.values():
            if entity.location == point:
                return entity
        return None

    def place(self, entity):
        self.contents[entity.id] = entity

    def map_is_OK(self, other: [MapEntity]):
        other_entities = other.get_entities()
        if not self.check_all_other_entities_are_valid(other_entities):
            return False
        return len(self.contents) == len(other_entities)

    def check_all_other_entities_are_valid(self, other_contents: [MapEntity]):
        other_entities_are_all_valid = True
        for map_entity in other_contents:
            if self.at_xy(map_entity.x, map_entity.y).name != map_entity.name:
                other_entities_are_all_valid = False
        return other_entities_are_all_valid

    def remove(self, id):
        entity = self.contents[id]
        entity.location = Location(None, None)

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
        return self.at_xy(location.x, location.y)

    def vision_at(self, location):
        result = []
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                found = self.at_xy(location.x + dx, location.y + dy)
                if found:
                    result.append((found.name, found.x, found.y))
        return result

    def scent_at(self, location):
        total_scent = 0
        for dx in (-2, -1, 0, 1, 2):
            for dy in (-2, -1, 0, 1, 2):
                current = location + Direction(dx, dy)
                scent = self.relative_scent(location, current)
                total_scent += scent
        return total_scent

    def relative_scent(self, location, current):
        found = self.at_xy(current.x, current.y)
        scent = 0
        if found and found.name == 'B':
            scent = 4 - location.distance(current)
            if scent < 0:
                scent = 0
        return scent
