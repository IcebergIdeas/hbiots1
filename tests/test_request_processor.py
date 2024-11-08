from client.request_builder import RequestBuilder


class ActionProcessor:
    def __init__(self, action):
        self.verb = action['verb']
        self.param1 = action['param1']

    def process(self):
        return f'    doing {self.verb} {self.param1}'


class RequestProcessor:
    def __init__(self, raw_rq):
        self.rq = raw_rq

    def actions(self):
        return self.rq['actions']

    def process(self):
        id = self.rq['entity']
        result = [f'for entity {id}:']
        for action in self.actions():
            action_processor = ActionProcessor(action)
            result.append(action_processor.process())
        return result


class MessageProcessor:
    def __init__(self, message: list):
        self.message = message

    def __iter__(self):
        for raw_rq in self.message:
            yield RequestProcessor(raw_rq)

    def process(self):
        result = []
        for rq in self:
            result.extend(rq.process())
        return result


class TestRequestProcessor:

    def message(self):
        builder = RequestBuilder()
        result = builder \
            .request(101) \
                .action('step') \
                .action('take') \
            .request(102) \
                .action('drop', 103) \
                .action('turn', 'EAST') \
                .action('step') \
            .result()
        return result

    def test_iteration(self):
        message = self.message()
        processor = MessageProcessor(message)
        count = 0
        for rq in processor:
            count += 1
        assert count == 2

    def test_process(self):
        message = self.message()
        processor = MessageProcessor(message)
        result = processor.process()
        assert result == [
            'for entity 101:',
             '    doing step None',
             '    doing take None',
             'for entity 102:',
             '    doing drop 103',
             '    doing turn EAST',
             '    doing step None']


