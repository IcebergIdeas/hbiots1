class RequestBuilder:
    def __init__(self):
        self._requests = []
        self._current_request = None
        self._current_actions = None

    def request(self, identifier):
        self._current_request = { 'entity': identifier }
        self._requests.append(self._current_request)
        self._current_actions = list()
        self._current_request['actions'] = self._current_actions
        return self

    def action(self, verb, parameter=None ):
        step = {'verb': verb, 'param1': parameter}
        self._current_actions.append(step)
        return self

    def result(self):
        return self._requests
