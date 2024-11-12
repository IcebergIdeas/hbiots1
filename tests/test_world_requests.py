from server.world import World
from server.world_entity import WorldEntity
from shared.direction import Direction
from shared.location import Location


class TestWorldRequests:
    def test_one_step(self):
        world = World(10, 10)
        bot_id = world.add_bot(5, 5)
        rq = { 'entity': bot_id, 'verb': 'step' }
        rq_list = [rq]
        world.execute(rq_list)
        world_bot = world.entity_from_id(bot_id)
        assert world_bot.location == Location(6, 5)

    def test_drop(self):
        world = World(10, 10)
        bot_id = world.add_bot(5, 5)
        block_id = world.add_block(6, 5)
        rq = [ {'entity': bot_id, 'verb': 'take'}]
        world.execute(rq)
        world_bot = world.entity_from_id(bot_id)
        assert world_bot.holding.id == block_id
        assert world.map.at_xy(6, 5) is None
        block = world.entity_from_id(block_id)
        rq = [ { 'entity': bot_id, 'verb': 'drop', 'param1': block_id } ]
        world.execute(rq)
        assert world.map.at_xy(6, 5) == block

    def test_bot_turns(self):
        world = World(10, 10)
        bot_id = world.add_bot(5, 5)
        bot = world.entity_from_id(bot_id)
        assert bot.direction == Direction.EAST
        rq = [ { 'entity': bot_id, 'verb': 'turn', 'param1': 'NORTH'}]
        world.execute(rq)
        assert bot.direction == Direction.NORTH

    def test_add_bot(self):
        WorldEntity.next_id = 100
        world = World(10, 10)
        command = {'entity': 0,
                   'verb': 'add_bot',
                   'x': 5,
                   'y': 6,
                   'direction': 'EAST'}
        rq = [ command ]
        result = world.execute(rq)
        assert len(result) == 1


    def test_returns_results(self):
        WorldEntity.next_id = 100
        world = World(10, 10)
        bot_1_id = world.add_bot(5, 5)
        bot_2_id = world.add_bot(7, 7, Direction.NORTH)
        rq =  [
            { 'entity': bot_1_id, 'verb': 'turn', 'param1': 'NORTH'},
            { 'entity': bot_1_id, 'verb': 'step'},
            { 'entity': bot_2_id, 'verb': 'step'},
            { 'entity': bot_2_id, 'verb': 'step'},
        ]
        result = world.execute(rq)
        assert len(result) == 2
        for d in result:
            print(d)
            match d['eid']:
                case 101:
                    assert d['location'] == Location(5, 4)
                case 102:
                    assert d['location'] == Location(7, 5)




