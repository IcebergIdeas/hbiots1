from collections import namedtuple

from direction import Direction
from location import Location
from world import World

EntityAction = namedtuple("EntityAction", "action parameter")

class EntityRequest:
    def __init__(self, entity_identifier, world_input=None):
        self.world_input = world_input
        self.entity_identifier = entity_identifier
        self.actions = []

    def add_action(self, action: EntityAction):
        self.actions.append(action)

    def action(self, action_word, parameter=None):
        self.add_action(EntityAction(action_word, parameter))
        return self

    def finish(self):
        return self.world_input

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

    def request(self, identifier):
        rq = EntityRequest(identifier, self)
        self.add_request(rq)
        return rq

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

    def test_more_action(self):
        world = World(10, 10)
        block_id = world.add_block(6, 5)
        bot_id = world.add_bot(5, 5, direction=Direction.EAST)
        request = EntityRequest(bot_id)
        request.add_action(EntityAction('take', None))
        request.add_action(EntityAction('turn', 'SOUTH'))
        request.add_action(EntityAction('step', None))  # 5, 6
        request.add_action(EntityAction('step', None))  # 5, 7
        request.add_action(EntityAction('drop', block_id))  # 5, 8
        batch_in = WorldInput()
        batch_in.add_request(request)
        batch_out = world.process(batch_in)
        result = batch_out.results[0]
        assert result['location'] == Location(5, 7)
        item = world.map.at_xy(5, 8)
        assert item.id == block_id

    def test_imaginary_syntax(self):
        world = World(10, 10)
        block_id = world.add_block(6, 5)
        batch_in = WorldInput() \
          .request(world.add_bot(5, 5)) \
              .action('take') \
              .action('turn','SOUTH') \
              .action('step') \
              .action('step') \
              .action('drop', block_id) \
              .finish() \
          .request(world.add_bot(7, 7)) \
              .action('step') \
              .action('step') \
              .finish()

    def test_new_syntax(self):
        world = World(10, 10)
        block_id = world.add_block(6, 5)
        batch_in = WorldInput() \
            .request(world.add_bot(5, 5, direction=Direction.EAST)) \
                .action('take', None) \
                .action('turn', 'SOUTH') \
                .action('step', None) \
                .action('step', None) \
                .action('drop', block_id) \
                .finish() \
            .request(world.add_bot(7, 7)) \
                .action('step') \
                .finish()
        batch_out = world.process(batch_in)
        result = batch_out.results[0]
        assert result['location'] == Location(5, 7)
        result = batch_out.results[1]
        assert result['location'] == Location(8, 7)
        item = world.map.at_xy(5, 8)
        assert item.id == block_id

    def test_two_bots_return_two_results(self):
        world = World(10, 10)
        bot_a = world.add_bot(5, 5, direction=Direction.EAST)
        bot_b = world.add_bot(7, 7, direction=Direction.WEST)
        request_a = EntityRequest(bot_a)
        request_b = EntityRequest(bot_b)
        batch_in = WorldInput()
        batch_in.add_request(request_a)
        batch_in.add_request(request_b)
        batch_out = world.process(batch_in)
        assert len(batch_out.results) == 2