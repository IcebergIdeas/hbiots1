class WorldEntity:
    def __init__(self):
        self._dict = dict()

    @property
    def id(self):
        return self._dict['id']

    @id.setter
    def id(self, value):
        self._dict['id'] = value

    @property
    def direction(self):
        return self._dict['direction']

    @direction.setter
    def direction(self, value):
        self._dict['direction'] = value

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
    def holding(self):
        return self._dict['holding']

    @holding.setter
    def holding(self, value):
        self._dict['holding'] = value

    def as_dictionary(self):
        return self._dict

    def receive(self, entity):
        self.holding = entity
