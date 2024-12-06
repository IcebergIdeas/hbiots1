from server.map import Map
from server.world_entity import WorldEntity
from shared.direction import Direction


class World:
    def __init__(self, max_x, max_y):
        self.map = Map(max_x, max_y)
        self.ids_used = set()
        self.messages = []

    def add_block(self, x, y, aroma=0):
        return self._add_entity(WorldEntity.block(x, y, aroma))

    def add_bot(self, x, y, direction = Direction.EAST):
        return self._add_entity(WorldEntity.bot(x, y, direction))

    def _add_entity(self, entity):
        self.map.place(entity)
        return entity.id

    def _add_message(self, msg):
        message_dict = { 'message': msg}
        self.messages.append(message_dict)

    def _add_bot_message(self, bot, msg):
        message_dict = { 'bot_id': bot.id, 'message': msg}
        self.messages.append(message_dict)

    def entity_from_id(self, bot_id):
        return self.map.at_id(bot_id)

    def execute_requests(self, actions_list):
        self.ids_used = set()
        self.messages = []
        valid_actions = self.get_valid_list(actions_list)
        self.execute_actions(valid_actions)
        updates = [self.fetch(bot_id) for bot_id in self.ids_used]
        return { 'updates': updates, 'messages': self.messages }

    def get_valid_list(self, actions_list):
        if isinstance(actions_list, list):
            return actions_list
        else:
            self._add_message('requests must be a list of actions')
            return []

    def execute_actions(self, actions_list):
        for action in actions_list:
            if isinstance(action, dict):
                action_with_parameters = self.assign_parameters(**action)
                self.execute_action(action_with_parameters)
            else:
                self._add_message(f'action must be dictionary {action}')

    def assign_parameters(self, entity=None, **parameters):
        if entity:
            self.ids_used.add(entity)
            parameters['entity_object'] = self.entity_from_id(entity)
        return parameters

    @property
    def all_verbs(self):
        return [
            'add_bot',
            'drop',
            'step',
            'take',
            'turn',
            'NORTH',
            'EAST',
            'SOUTH',
            'WEST',
        ]

    def execute_action(self, action_dictionary):
        match action_dictionary:
            case {'verb': 'add_bot',
                  'x': x, 'y': y, 'direction': direction}:
                self.add_bot_action(x, y, direction)

            case {'verb': 'drop',
                  'entity_object': entity_object,
                  'holding': holding}:
                self.drop_forward_action(entity_object, holding)

            case {'verb': 'step',
                  'entity_object': entity_object}:
                self.step_action(entity_object)

            case {'verb': 'take',
                  'entity_object': entity_object}:
                self.take_forward_action(entity_object)

            case {'verb': 'turn',
                  'entity_object': entity_object,
                  'direction': 'NORTH' | 'EAST' | 'SOUTH' | 'WEST' as direction}:
                self.turn_action(entity_object, direction)
            case {'verb': 'turn',
                  'direction': bad_direction}:
                self._add_message(f'unknown direction {bad_direction}, should be NORTH, EAST, SOUTH, or WEST')

            case {'verb': 'NORTH' | 'EAST' | 'SOUTH' | 'WEST' as direction,
                  'entity_object': entity_object}:
                self.turn_action(entity_object, direction)

            case { 'verb': verb } if verb not in self.all_verbs:
                self._add_message(f'unknown verb: {verb}')
            case { 'verb': verb} if verb not in ['add_bot',]:
                self._add_message(f'verb {verb} requires entity parameter {action_dictionary}')
            case _:
                self._add_message(f'Unknown action {action_dictionary}')

    def add_bot_action(self, x, y, direction):
        bot_id = self.add_bot(x, y, Direction.from_name(direction))
        self.ids_used.add(bot_id)

    def drop_forward_action(self, bot, holding):
        self.drop_forward(bot, self.entity_from_id(holding))

    def drop_forward(self, bot, held_entity):
        if self.map.place_at(held_entity, bot.forward_location()):
            bot.remove(held_entity)
        else:
            self._add_bot_message(bot, 'drop location was not open')

    def step_action(self, bot):
        self.map.attempt_move(bot.id, bot.forward_location())  # changes world version
        self.set_bot_vision(bot)
        self.set_bot_scent(bot)

    def take_forward_action(self, bot):
        is_block = lambda e: e.name == 'B'
        if block := self.map.take_conditionally_at(bot.forward_location(), is_block):
            bot.receive(block)

    def turn_action(self, world_bot, direction_name):
        # no change on unrecognized name
        if direction_name in ['NORTH', 'EAST', 'SOUTH', 'WEST']:
            world_bot.direction = Direction.from_name(direction_name)

    def fetch(self, entity_id):
        return self.entity_from_id(entity_id).as_dictionary()

    def set_bot_vision(self, bot):
        bot.vision = self.map.vision_at(bot.location)

    def set_bot_scent(self, bot):
        aroma_to_seek = 0
        if bot.holding:
            aroma_to_seek = bot.holding.aroma
        bot.scent = self.map.scent_at(bot.location, aroma_to_seek)

    def is_empty(self, drop_location):
        return not self.map.at_xy(drop_location.x, drop_location.y)
