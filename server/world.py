from server.map import Map
from server.world_entity import WorldEntity
from shared.direction import Direction


class World:
    def __init__(self, max_x, max_y):
        self.width = max_x
        self.height = max_y
        self.map = Map(max_x, max_y)
        self.ids_used = set()

    def add_block(self, x, y, aroma=0):
        return self._add_entity(WorldEntity.block(x, y, aroma))

    def add_bot(self, x, y, direction = Direction.EAST):
        return self._add_entity(WorldEntity.bot(x, y, direction))

    def _add_entity(self, entity):
        self.map.place(entity)
        return entity.id

    def entity_from_id(self, bot_id):
        return self.map.at_id(bot_id)

    def execute(self, actions_list):
        self.ids_used = set()
        for action in actions_list:
            self.unpack_and_execute(**action)
        return [ self.fetch(bot_id) for bot_id in self.ids_used ]

    def unpack_and_execute(self, entity, verb, **parameters):
        if entity:
            self.ids_used.add(entity)
            entity_object = self.entity_from_id(entity)
        else:
            entity_object = None
        self.execute_action(entity_object, verb, parameters)

    def execute_action(self, entity, verb, parameters):
        match verb:
            case 'add_bot':
                self.add_bot_action(**parameters)
            case 'step':
                self.step(entity)
            case 'take':
                self.take_forward(entity)
            case 'drop':
                self.drop_forward_action(entity, **parameters)
            case 'NORTH' | 'EAST' | 'SOUTH' | 'WEST' as direction:
                self.set_direction(entity, direction)
            case 'turn':
                direction = parameters['direction']
                self.set_direction(entity, direction)
            case _:
                raise Exception(f'Unknown action {verb}')

    def drop_forward_action(self, entity, holding, **_):
        self.drop_forward(entity, self.entity_from_id(holding))

    def add_bot_action(self, x, y, direction, **_):
        bot_id = self.add_bot(x, y, Direction.from_name(direction))
        self.ids_used.add(bot_id)

    def fetch(self, entity_id):
        return self.entity_from_id(entity_id).as_dictionary()

    def set_direction(self, world_bot, direction_name):
        # no change on unrecognized name
        if direction_name in ['NORTH', 'EAST', 'SOUTH', 'WEST']:
            world_bot.direction = Direction.from_name(direction_name)

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
