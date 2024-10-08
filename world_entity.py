from direction import Direction
from entity_kind import EntityKind
from location import Location


class WorldEntity:
    next_id = 100

    def __init__(self, kind: EntityKind, x: int, y: int, direction: Direction):
        self._dict = dict()
        WorldEntity.next_id += 1
        self._dict['eid'] = self.next_id
        self._dict['kind'] = kind
        self.aroma = 0
        self.location = Location(x, y)
        self.direction = direction
        self.holding = None
        self.scent = 0
        self.vision = []

    @classmethod
    def bot(cls, x, y, direction):
        return cls(EntityKind.BOT, x, y, direction)

    @classmethod
    def block(cls, x, y):
        return cls(EntityKind.BLOCK, x, y, Direction.EAST)

    @property
    def aroma(self):
        return self._dict['aroma']

    @aroma.setter
    def aroma(self, aroma):
        self._dict['aroma'] = aroma

    @property
    def id(self):
        return self._dict['eid']

    @property
    def direction(self):
        return self._dict['direction']

    @direction.setter
    def direction(self, value):
        self._dict['direction'] = value

    @property
    def kind(self):
        return self._dict['kind']

    @property
    def name(self):
        return 'R' if self.kind is EntityKind.BOT else 'B'

    @property
    def location(self):
        return self._dict['location']

    @location.setter
    def location(self, value):
        self._dict['location'] = value

    @property
    def scent(self):
        return self._dict['scent']

    @scent.setter
    def scent(self, value):
        self._dict['scent'] = value

    @property
    def vision(self):
        return self._dict['vision']

    @vision.setter
    def vision(self, value):
        self._dict['vision'] = value

    @property
    def x(self):
        return self.location.x

    @property
    def y(self):
        return self.location.y

    @property
    def holding(self):
        try:
            return self._dict['held_entity']
        except KeyError:
            return None

    @holding.setter
    def holding(self, value):
        self._dict['held_entity'] = value

    def as_dictionary(self):
        return self._dict

    def forward_location(self):
        return self.location + self.direction

    def has(self, entity):
        return self.holding is entity

    def has_block(self):
        return self.holding.kind is EntityKind.BLOCK

    def receive(self, entity):
        self.holding = entity

    def remove(self, entity):
        if self.holding is entity:
            self.holding = None
