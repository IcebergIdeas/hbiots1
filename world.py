from direction import Direction
from map import Map
from world_entity import WorldEntity


class World:
    next_id = 100

    def __init__(self, max_x, max_y):
        self.width = max_x
        self.height = max_y
        self.map = Map(max_x, max_y)

    def add_block(self, x, y, aroma=0):
        entity = WorldEntity.block(x, y, aroma)
        self.map.place(entity)
        return entity.id

    def add_bot(self, x, y, direction = Direction.EAST):
        entity = WorldEntity.bot(x, y, direction)
        self.map.place(entity)
        return entity.id

    def add_and_return_client_entity(self, entity, returned_client_entity):
        self.map.place(entity)
        id = entity.id
        returned_client_entity.id = id
        return returned_client_entity

    def command(self, action, bot_id, parameter=None):
        world_bot = self.entity_from_id(bot_id)
        if action == 'step':
            self.step(world_bot)
        elif action == 'take':
            self.take_forward(world_bot)
        elif action == 'drop':
            block = self.entity_from_id(parameter)
            self.drop_forward(world_bot, block)
        elif action == 'turn':
            self.set_direction(world_bot, parameter)
        else:
            raise Exception(f'Unknown command {action}')

    def entity_from_id(self, bot_id):
        return self.map.at_id(bot_id)

    def fetch(self, entity_id):
        return self.entity_from_id(entity_id).as_dictionary()

    def set_direction(self, world_bot, direction_name):
        match direction_name:
            case 'NORTH':
                world_bot.direction = Direction.NORTH
            case 'EAST':
                world_bot.direction = Direction.EAST
            case 'WEST':
                world_bot.direction = Direction.WEST
            case 'SOUTH':
                world_bot.direction = Direction.SOUTH
            case _:
                pass

    def step(self, bot):
        self.map.attempt_move(bot.id, bot.forward_location())  # changes world version
        self.set_bot_vision(bot)
        self.set_bot_scent(bot)

    def set_bot_vision(self, bot):
        bot.vision = self.map.vision_at(bot.location)

    def set_bot_scent(self, bot):
        aroma_to_seek = 0
        if bot.holding:
            aroma_to_seek = bot.holding.aroma
        bot.scent = self.map.scent_at(bot.location, aroma_to_seek)

    def take_forward(self, bot):
        is_block = lambda e: e.name == 'B'
        if block := self.map.take_conditionally_at(bot.forward_location(), is_block):
            bot.receive(block)

    def drop_forward(self, bot, entity):
        if self.map.place_at(entity, bot.forward_location()):
            bot.remove(entity)

    def is_empty(self, drop_location):
        return not self.map.at_xy(drop_location.x, drop_location.y)

    def update_client_for_test(self, client_bot):
        result_dict = self.fetch(client_bot.id)
        client_bot._knowledge.update(result_dict)

    def process(self, world_input):
        from test_world_batch import WorldOutput
        output = WorldOutput()
        for request in world_input:
            requestor_id = request.identifier
            for action in request:
                self.command(action.action, requestor_id, action.parameter)
            output.append(self.fetch(requestor_id))
        return output
