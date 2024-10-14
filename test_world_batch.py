from collections import namedtuple

from direction import Direction
from location import Location
from world import World

EntityAction = namedtuple("EntityAction", "action parameter")

class EntityRequest:
    def __init__(self, entity_identifier):
        self.entity_identifier = entity_identifier
        self.actions = []

    def add_action(self, action: EntityAction):
        self.actions.append(action)

    @property
    def identifier(self):
        return self.entity_identifier

    def __iter__(self):
        return iter(self.actions)


class WorldInput:
    def __init__(self):
        self.requests = []

    def __iter__(self):
        return iter(self.requests)

    def add_request(self, request: EntityRequest):
        self.requests.append(request)


class WorldOutput:
    def __init__(self):
        self.results = []

    def is_empty(self):
        return self.results == []

    def append(self, fetch_result):
        self.results.append(fetch_result)


class TestWorldBatch:
    def test_empty_batch(self):
        world = World(10, 10)
        batch_in = WorldInput()
        batch_out = world.process(batch_in)
        assert isinstance(batch_out, WorldOutput)
        assert batch_out.is_empty()

    def test_step(self):
        world = World(10, 10)
        bot_id = world.add_bot(5, 5, direction=Direction.EAST)
        request = EntityRequest(bot_id)
        step_action = EntityAction('step', None)
        request.add_action(step_action)
        batch_in = WorldInput()
        batch_in.add_request(request)
        batch_out = world.process(batch_in)
        assert isinstance(batch_out, WorldOutput)
        # invasive just to see how we did
        result = batch_out.results[0]
        assert result['location'] == Location(6, 5)
