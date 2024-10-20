from vision import Vision


class NewKnowledge:
    drop_threshold = 4
    take_threshold = 7
    energy_threshold = 5

    def __init__(self, location=None, direction=None):
        self._dict = dict()
        self.location = location
        self.direction = direction
        self.use_energy()

    def __getattr__(self, item):
        return self._dict[item]

    def __setattr__(self, key, value):
        known = ['_energy', 'id', '_scent', 'location', 'direction', 'held_entity', 'vision']
        if key == '_dict':
            return super().__setattr__(key, value)
        if key in known:
            self._dict[key] = value
        else:
            raise AttributeError(f'{key} not in {known}')

    def update(self, update_dictionary):
        self.direction = update_dictionary['direction']
        self.held_entity = update_dictionary['held_entity']
        self.id = update_dictionary['eid']
        self.location = update_dictionary['location']
        self._scent = update_dictionary['scent']
        self.vision = Vision(update_dictionary['vision'], self.location, self.direction)

    def has(self, entity):
        return entity == self.held_entity

    @property
    def has_block(self):
        return self.held_entity is not 0

    def has_energy(self):
        return self._energy >= self.energy_threshold

    @property
    def holding(self):
        return self.held_entity

    def use_energy(self):
        self._energy = 0

    def gain_energy(self):
        self._energy = self._energy + 1

    def receive(self, entity):
        self.held_entity = entity

    def remove(self, entity):
        if self.held_entity == entity:
            self.held_entity = None
