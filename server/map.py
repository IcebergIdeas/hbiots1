from server.map_test_entity import MapTestEntity
from server.world_entity import WorldEntity
from shared.direction import Direction
from shared.location import Location


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

    def place_at(self, entity, drop_location):
        if self.location_is_open(drop_location):
            entity.location = drop_location
            self.place(entity)
            return True
        else:
            return False

    def place(self, entity):
        assert isinstance(entity, WorldEntity)
        self.contents[entity.key] = entity

    def map_is_OK(self, other: [MapTestEntity]):
        other_entities = other.get_entities()
        if not self.check_all_other_entities_are_valid(other_entities):
            return False
        return len(self.contents) == len(other_entities)

    def check_all_other_entities_are_valid(self, other_contents: [MapTestEntity]):
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
        if self.location_is_open(location):
            entity.location = location

    def location_is_open(self, location: Location):
        return self.is_within_map(location) and not self.is_occupied(location)

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

    def scent_at(self, location, desired_aroma):
        total_scent = 0
        for dx in (-2, -1, 0, 1, 2):
            for dy in (-2, -1, 0, 1, 2):
                current = location + Direction(dx, dy)
                scent = self.relative_scent(location, current, desired_aroma)
                total_scent += scent
        return total_scent

    def relative_scent(self, location, current, desired_aroma):
        found = self.at_xy(current.x, current.y)
        scent = 0
        if found and found.name == 'B' and found.aroma == desired_aroma:
            scent = 4 - location.distance(current)
            if scent < 0:
                scent = 0
        return scent

    def take_conditionally_at(self, take_location, condition):
        item = self.at_xy(take_location.x, take_location.y)
        if item and condition(item):
            self.remove(item.key)
            return item
        else:
            return None
