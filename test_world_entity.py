from direction import Direction
from location import Location
from world_entity import WorldEntity


class TestWorldEntity:
    def is_valid(self, entity):
        assert entity._dict['id'] == entity.id
        assert entity._dict['direction'] == entity.direction
        assert entity._dict['held_entity'] == entity.holding
        assert entity._dict['location'] == entity.location
        assert entity._dict['scent'] == entity.scent
        assert entity._dict['vision'] == entity.vision
        return True

    def test_create(self):
        WorldEntity()

    def test_set_and_fetch(self):
        entity = WorldEntity()
        entity.id = 102
        assert entity.id == 102
        entity.direction = Direction.EAST
        assert entity.direction == Direction.EAST
        entity.location = Location(6,4)
        assert entity.location == Location(6,4)
        entity.receive("hello")
        assert entity.holding == "hello"
        entity.scent = 37
        assert entity.scent == 37
        entity.vision = []
        assert entity.vision == []
        assert self.is_valid(entity)
        assert entity.as_dictionary() is entity._dict