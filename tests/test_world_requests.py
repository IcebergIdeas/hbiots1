from server.world import World
from shared.direction import Direction
from shared.location import Location


class TestWorldRequests:
    def test_hookup(self):
        assert True

    def test_imaginary_request(self):
        single_request = {
            "entity": 100,
            "actions": [
                {"verb": "take"},
                {"verb": 'step'}
            ]
        }
        id = single_request['entity']
        assert id == 100
        first_action = single_request['actions'][0]
        assert first_action['verb'] == 'take'

    def test_one_step(self):
        world = World(10, 10)
        bot_id = world.add_bot(5, 5)
        rq = {
            'entity': bot_id,
            'actions': [
                {'verb': 'step'}
            ]
        }
        world.execute(rq)
        world_bot = world.entity_from_id(bot_id)
        assert world_bot.location == Location(6, 5)

    def test_drop(self):
        world = World(10, 10)
        bot_id = world.add_bot(5, 5)
        block_id = world.add_block(6, 5)
        rq = {
            'entity': bot_id,
            'actions': [
                {'verb': 'take'}
            ]
        }
        world.execute(rq)
        world_bot = world.entity_from_id(bot_id)
        assert world_bot.holding.id == block_id
        assert world.map.at_xy(6, 5) is None
        block = world.entity_from_id(block_id)
        rq = {
            'entity': bot_id,
            'actions': [
                {'verb': 'drop', 'param1': block_id}
            ]
        }
        world.execute(rq)
        assert world.map.at_xy(6, 5) == block

    def test_bot_turns(self):
        world = World(10, 10)
        bot_id = world.add_bot(5, 5)
        bot = world.entity_from_id(bot_id)
        assert bot.direction == Direction.EAST
        rq = {
            'entity': bot_id,
            'actions': [
                {'verb': 'turn', 'param1': 'NORTH'}
            ]
        }
        world.execute(rq)
        assert bot.direction == Direction.NORTH


