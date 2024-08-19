from map_entry import MapEntity
from point import Point


class Entities:
    def __init__(self):
        self.contents = {}

    def place(self, biot):
        self.contents[biot.id] = biot

    def entity_at(self, x, y):
        point = Point(x, y)
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


