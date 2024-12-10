from server.map import Map
from server.world_entity import WorldEntity
from shared.direction import Direction


class World:
    error_messages = {
        'TURN_DIRECTION':
            'unknown direction {direction}, should be NORTH, EAST, SOUTH, or WEST',
        'VERB_NEEDS_BOT_KEY':
            'verb {verb} requires bot_key parameter {details}'
    }

    def __init__(self, max_x, max_y):
        self.map = Map(max_x, max_y)
        self.ids_used = set()
        self.messages = []

    def add_block(self, x, y, aroma=0):
        return self._add_entity(WorldEntity.block(x, y, aroma))

    def _add_entity(self, entity):
        self.map.place(entity)
        return entity.key

    def _add_completed_message(self, msg):
        message_dict = { 'message': msg}
        self.messages.append(message_dict)

    def _add_bot_message(self, bot, msg):
        message_dict = { 'bot_id': bot.key, 'message': msg}
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
            self._add_completed_message('requests must be a list of actions')
            return []

    def execute_actions(self, actions_list):
        for action in actions_list:
            if isinstance(action, dict):
                action_with_parameters = self.assign_parameters(**action)
                self.execute_action(**action_with_parameters)
            else:
                self._add_completed_message(f'action must be dictionary {action}')

    def assign_parameters(self, bot_key=None, **parameters):
        if bot_key:
            self.ids_used.add(bot_key)
            parameters['bot'] = self.entity_from_id(bot_key)
        return parameters

    def execute_action(self, verb=None, bot=None, **details):
        if not bot and verb != 'add_bot':
            self._add_keyed_message(
                'VERB_NEEDS_BOT_KEY',
                verb=verb, details=details)
        else:
            self.execute_verb(verb, bot, details)

    def execute_verb(self, verb, bot, details):
        match verb:
            case 'add_bot':
                self.add_bot_using(**details)
            case 'step':
                self.step(bot)
            case 'drop':
                self.drop_using(bot, **details)
            case 'take':
                self.take_forward(bot)
            case 'turn':
                self.turn_using(bot, **details)
            case 'NORTH' | 'EAST' | 'SOUTH' | 'WEST' as direction:
                self.turn(bot, direction)
            case _:
                self._add_completed_message(f'Unknown action {verb=} {details=}')

    def add_bot_using(self, x=None, y=None, direction=None, **ignored):
        if self.add_bot_check_parameters(x, y, direction):
            self.add_bot_action(x, y, direction)

    def add_bot_check_parameters(self, x, y, direction):
        if not x or not y:
            self._add_completed_message('add_bot command requires x and y parameters')
            return False
        if direction not in Direction.ALL_NAMES:
            self._add_completed_message(f'add_bot has unknown direction {direction},'
                              f' should be NORTH, EAST, SOUTH, or WEST')
            return False
        return True

    def add_bot_action(self, x, y, direction):
        bot_id = self.add_bot(x, y, Direction.from_name(direction))
        self.ids_used.add(bot_id)

    def add_bot(self, x, y, direction = Direction.EAST):
        return self._add_entity(WorldEntity.bot(x, y, direction))

    def drop_using(self, bot, holding=None, **ignored):
        self.drop_forward_action(bot, holding)

    def drop_forward_action(self, bot, holding):
        self.drop_forward(bot, self.entity_from_id(holding))

    def drop_forward(self, bot, held_entity):
        if self.map.place_at(held_entity, bot.forward_location()):
            bot.remove(held_entity)
        else:
            self._add_bot_message(bot, 'drop location was not open')

    def step(self, bot):
        self.map.attempt_move(bot.key, bot.forward_location())  # changes world version
        self.set_bot_vision(bot)
        self.set_bot_scent(bot)

    def take_forward(self, bot):
        is_block = lambda e: e.name == 'B'
        if block := self.map.take_conditionally_at(bot.forward_location(), is_block):
            bot.receive(block)

    def turn_using(self, bot, direction=None, **ignored):
        match direction:
            case 'NORTH' | 'EAST' | 'SOUTH' | 'WEST':
                self.turn(bot, direction)
            case _:
                self._add_keyed_message("TURN_DIRECTION", direction=direction)

    def _add_keyed_message(self, key, **kwargs):
        msg = self._get_message(key)
        formatted = msg.format(**kwargs)
        self._add_completed_message(formatted)

    def _get_message(self, key):
        return key + ": " + self.error_messages.get(key, key)

    def turn(self, world_bot, direction_name):
        # no change on unrecognized name
        if direction_name in Direction.ALL_NAMES:
            world_bot.direction = Direction.from_name(direction_name)

    def fetch(self, bot_key):
        return self.entity_from_id(bot_key).as_dictionary()

    def set_bot_vision(self, bot):
        bot.vision = self.map.vision_at(bot.location)

    def set_bot_scent(self, bot):
        aroma_to_seek = 0
        if bot.holding:
            aroma_to_seek = bot.holding.aroma
        bot.scent = self.map.scent_at(bot.location, aroma_to_seek)

    def is_empty(self, drop_location):
        return not self.map.at_xy(drop_location.x, drop_location.y)
