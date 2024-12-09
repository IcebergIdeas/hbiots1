from server.entity_kind import EntityKind
from server.world_entity import WorldEntity
from shared.direction import Direction
from shared.location import Location


class TestWorldEntity:
    def is_valid(self, entity):
        assert entity._dict['key'] == entity.key
        assert entity._dict['direction'] == entity.direction
        assert entity._dict['held_entity'] == entity.holding
        assert entity._dict['location'] == entity.location
        assert entity._dict['scent'] == entity.scent
        assert entity._dict['vision'] == entity.vision
        return True

    def test_create(self):
        entity = WorldEntity(EntityKind.BOT, 6, 4, Direction.EAST)
        assert entity.kind == EntityKind.BOT

    def test_set_and_fetch(self):
        # not much of a test really
        entity = WorldEntity.bot(0, 0, Direction.EAST)
        assert entity.direction == Direction.EAST
        entity.location = Location(6, 4)
        assert entity.location == Location(6,4)
        block = WorldEntity.block(9, 9, 0)
        entity.receive(block)
        assert entity.holding == block
        entity.scent = 37
        assert entity.scent == 37
        entity.vision = []
        assert entity.vision == []
        assert self.is_valid(entity)
        fetched = entity.as_dictionary()
        assert fetched['key'] == entity.key
        assert fetched['direction'] == Direction.EAST
        assert fetched['held_entity'] == block.key
        assert fetched['location'] == Location(6, 4)
        assert fetched['scent'] == 37
        assert fetched['vision'] == []

    def test_create_block(self):
        entity = WorldEntity.block(0, 0, 0)