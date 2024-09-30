from bot import Bot
from direction import Direction
from map import Map


class World:
    next_id = 100

    def __init__(self, max_x, max_y):
        self.width = max_x
        self.height = max_y
        self.map = Map(max_x, max_y)

    def add_bot(self, x, y, direction = Direction.EAST):
        id = self.add_world_bot(x, y, direction)
        returned_bot = Bot(x, y, direction)
        returned_bot.id = id
        returned_bot.world = self
        return returned_bot

    def add_world_bot(self, x, y, direction = Direction.EAST):
        bot = Bot(x, y, direction)
        self.add(bot)
        return bot.id

    def add(self, entity):
        entity.world = self
        World.next_id += 1
        entity.id = World.next_id
        self.map.place(entity)

    def command(self, action, bot_id, parameter=None):
        world_bot = self.map.at_id(bot_id)
        if action == 'step':
            self.step(world_bot)
        elif action == 'take':
            self.take_forward(world_bot)
        elif action == 'drop':
            block = self.map.at_id(parameter)
            self.drop_forward(world_bot, block)
        elif action == 'turn':
            self.set_direction(world_bot, parameter)
        else:
            raise Exception('Unknown command')

    def fetch(self, entity_id):
        return self.map.at_id(entity_id)._knowledge.as_dictionary()

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
        location = self.bots_next_location(bot)
        self.map.attempt_move(bot.id, location)  # changes world version
        real_bot = self.map.at_id(bot.id)
        self.set_bot_vision(real_bot)
        self.set_bot_scent(real_bot)

    def set_bot_vision(self, bot):
        bot.vision = self.map.vision_at(bot.location)

    def set_bot_scent(self, bot):
        bot.scent = self.map.scent_at(bot.location)

    def clip(self, coord, limit):
        return 0 if coord < 0 else (limit if coord > limit else coord)

    def take_forward(self, bot: Bot):
        take_location = self.bots_next_location(bot)
        if take_location == bot.location:
            return
        entity = self.map.at_xy(take_location.x, take_location.y)
        if self.can_take_entity(entity):
            self.map.remove(entity.id)
            bot.receive(entity)

    def can_take_entity(self, entity):
        return entity and entity.name != 'R'

    def drop_forward(self, bot, entity):
        drop_location = bot.location + bot.direction
        if self.map.location_is_open(drop_location):
            entity.location = drop_location
            bot.remove(entity)

    def is_empty(self, drop_location):
        return not self.map.at_xy(drop_location.x, drop_location.y)

    def bots_next_location(self, bot):
        location = bot.location + bot.direction
        return bot.location if self.is_off_world(location) else location

    def is_off_world(self, location):
        return self.clip(location.x, self.width) != location.x \
            or self.clip(location.y, self.height) != location.y

    def update_client_for_test(self, client_bot):
        result_dict = self.fetch(client_bot.id)
        client_bot._knowledge.update(result_dict)
