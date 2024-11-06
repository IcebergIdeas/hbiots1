from collections import namedtuple

EntityAction = namedtuple("EntityAction", "action parameter")

class EntityRequest:
    def __init__(self, entity_identifier, world_input=None):
        self._world_input = world_input
        self._entity_identifier = entity_identifier
        self._actions = []

    def add_action(self, action: EntityAction):
        self._actions.append(action)

    @property
    def identifier(self):
        return self._entity_identifier

    def __iter__(self):
        return iter(self._actions)


class WorldInput:
    def __init__(self):
        self._requests = []

    def __iter__(self):
        return iter(self._requests)

    def add_request(self, request: EntityRequest):
        self._requests.append(request)

class WorldOutput:
    def __init__(self):
        self.results = []

    def is_empty(self):
        return self.results == []

    def append(self, fetch_result):
        self.results.append(fetch_result)