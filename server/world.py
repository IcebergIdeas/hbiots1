from server.map import Map
from server.world_entity import WorldEntity
from shared.direction import Direction


class World:
    next_id = 100

    def __init__(self, max_x, max_y):
        self.width = max_x
        self.height = max_y
        self.map = Map(max_x, max_y)
        self.ids_used = set()

    def add_block(self, x, y, aroma=0):
        entity = WorldEntity.block(x, y, aroma)
        self.map.place(entity)
        return entity.id

    def add_bot(self, x, y, direction = Direction.EAST):
        entity = WorldEntity.bot(x, y, direction)
        self.map.place(entity)
        return entity.id

    def entity_from_id(self, bot_id):
        return self.map.at_id(bot_id)

    def execute(self, actions_list):
        self.ids_used = set()
        for action in actions_list:
            id = action['entity']
            if id:
                self.ids_used.add(id)
                entity = self.entity_from_id(id)
            else:
                entity = None
            verb = action['verb']
            self.execute_action(entity, verb, action)
        return [ self.fetch(bot_id) for bot_id in self.ids_used ]

    def execute_action(self, entity, verb, action):
        match verb:
            case 'add_bot':
                bot_id = self.add_bot(action['x'], action['y'], action['direction'])
                self.ids_used.add(bot_id)
            case 'step':
                self.step(entity)
            case 'take':
                self.take_forward(entity)
            case 'drop':
                holding_id = action['holding']
                holding = self.entity_from_id(holding_id)
                self.drop_forward(entity, holding)
            case 'NORTH' | 'EAST' | 'SOUTH' | 'WEST' as direction:
                self.set_direction(entity, direction)
            case 'turn':
                direction = action['direction']
                self.set_direction(entity, direction)
            case _:
                raise Exception(f'Unknown action {verb}')

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
