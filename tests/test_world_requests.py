from server.world import World
from server.world_entity import WorldEntity
from shared.direction import Direction
from shared.location import Location


class TestWorldRequests:
    def test_one_step(self):
        world = World(10, 10)
        bot_id = world.add_bot(5, 5)
        rq = { 'bot_key': bot_id, 'verb': 'step' }
        rq_list = [rq]
        world.execute_requests(rq_list)
        world_bot = world.entity_from_id(bot_id)
        assert world_bot.location == Location(6, 5)

    def test_drop(self):
        world = World(10, 10)
        bot_id = world.add_bot(5, 5)
        block_id = world.add_block(6, 5)
        rq = [ {'bot_key': bot_id, 'verb': 'take'}]
        world.execute_requests(rq)
        world_bot = world.entity_from_id(bot_id)
        assert world_bot.holding.key == block_id
        assert world.map.at_xy(6, 5) is None
        block = world.entity_from_id(block_id)
        rq = [ { 'bot_key': bot_id, 'verb': 'drop', 'holding': block_id } ]
        world.execute_requests(rq)
        assert world.map.at_xy(6, 5) == block

    def test_bot_turns(self):
        world = World(10, 10)
        bot_id = world.add_bot(5, 5)
        bot = world.entity_from_id(bot_id)
        assert bot.direction == Direction.EAST
        rq = [ { 'bot_key': bot_id, 'verb': 'turn', 'direction': 'NORTH'}]
        world.execute_requests(rq)
        assert bot.direction == Direction.NORTH

    def test_turn_with_excess_parameters(self):
        world = World(10, 10)
        bot_id = world.add_bot(5, 5)
        bot = world.entity_from_id(bot_id)
        assert bot.direction == Direction.EAST
        rq = [ { 'bot_key': bot_id, 'verb': 'turn', 'direction': 'NORTH', 'spurious': 'extra'}]
        world.execute_requests(rq)
        assert bot.direction == Direction.NORTH

    def test_bot_direction_verbs(self):
        world = World(10, 10)
        bot_id = world.add_bot(5, 5)
        bot = world.entity_from_id(bot_id)
        choices = [ ('NORTH', Direction.NORTH),
                    ('EAST', Direction.EAST),
                    ('SOUTH', Direction.SOUTH),
                    ('WEST', Direction.WEST) ]
        for verb, result in choices:
            rq = [ { 'bot_key': bot_id, 'verb': verb } ]
            world.execute_requests(rq)
            assert bot.direction == result

    def test_add_bot(self):
        WorldEntity.next_key = 100
        world = World(10, 10)
        command = {'bot_key': 0,
                   'verb': 'add_bot',
                   'x': 5,
                   'y': 6,
                   'direction': 'EAST'}
        rq = [ command ]
        result = world.execute_requests(rq)['updates']
        assert len(result) == 1
        bot_info = result[0]
        assert bot_info['key'] == WorldEntity.next_key
        assert bot_info['location'] == Location(5, 6)

    def test_add_bot_with_spurious_parameter(self):
        WorldEntity.next_key = 100
        world = World(10, 10)
        command = {'bot_key': 0,
                   'verb': 'add_bot',
                   'x': 5,
                   'y': 6,
                   'direction': 'EAST',
                   'spurious': 'extra'}
        rq = [ command ]
        result = world.execute_requests(rq)['updates']
        assert len(result) == 1
        bot_info = result[0]
        assert bot_info['key'] == WorldEntity.next_key
        assert bot_info['location'] == Location(5, 6)

    def test_zero_id(self):
        WorldEntity.next_key = 100
        world = World(10, 10)
        command = {'bot_key': 0,
                   'verb': 'step'}
        rq = [ command ]
        messages = world.execute_requests(rq)['messages']
        assert 'VERB_NEEDS_BOT_KEY' in messages[0]['message']

    def test_returns_results(self):
        WorldEntity.next_key = 100
        world = World(10, 10)
        bot_1_id = world.add_bot(5, 5)
        bot_2_id = world.add_bot(7, 7, Direction.NORTH)
        rq =  [
            { 'bot_key': bot_1_id, 'verb': 'turn', 'direction': 'NORTH'},
            { 'bot_key': bot_1_id, 'verb': 'step'},
            { 'bot_key': bot_2_id, 'verb': 'step'},
            { 'bot_key': bot_2_id, 'verb': 'step'},
        ]
        result = world.execute_requests(rq)['updates']
        assert len(result) == 2
        for d in result:
            # print(d)
            match d['key']:
                case 101:
                    assert d['location'] == Location(5, 4)
                case 102:
                    assert d['location'] == Location(7, 5)





