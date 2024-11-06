from server.world import World
from server.world_entity import WorldEntity
from shared.direction import Direction
from shared.location import Location


class RequestBuilder:
    def __init__(self):
        self._requests = []
        self._current_request = None
        self._current_actions = None

    def request(self, identifier):
        self._current_request = { 'entity': identifier }
        self._requests.append(self._current_request)
        self._current_actions = list()
        self._current_request['actions'] = self._current_actions
        return self

    def action(self, verb, parameter=None ):
        step = {'verb': verb, 'param1': parameter}
        self._current_actions.append(step)
        return self

    def result(self):
        return self._requests


class TestRequestBuilder:
    def test_new_syntax_for_raw_collections(self):
        WorldEntity.next_id = 100
        world = World(10, 10)
        block_id = world.add_block(6, 5)  # 101
        batch_in = RequestBuilder() \
            .request(world.add_bot(5, 5, direction=Direction.EAST)) \
            .action('take', None) \
            .action('turn', 'SOUTH') \
            .action('step', None) \
            .action('step', None) \
            .action('drop', block_id) \
            .request(world.add_bot(7, 7)) \
            .action('step') \
            .result()
        assert len(batch_in) == 2
        rq_0 = batch_in[0]
        assert rq_0['entity'] == 102
        assert len(rq_0['actions']) == 5
        batch_out = world.process(batch_in)
        result = batch_out[0]
        assert result['location'] == Location(5, 7)
        result = batch_out[1]
        assert result['location'] == Location(8, 7)
        item = world.map.at_xy(5, 8)
        assert item.id == block_id