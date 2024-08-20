class Queue:
    def __init__(self):
        self._contents = []

    def put(self, item):
        self._contents.append(item)

    def get(self):
        return self._contents.pop(0)


class TestPathing:
    def test_hookup(self):
        assert 2 + 2 == 4

    def test_queue(self):
        q = Queue()
        q.put(2)
        assert q.get() == 2

    def test_queue_more(self):
        q = Queue()
        q.put(2)
        q.put(5)
        assert q.get() == 2
        assert q.get() == 5
