from world import World


class WorldInput:
    pass

    def __iter__(self):
        return iter([])


class WorldOutput:
    def is_empty(self):
        return True

    def append(self, fetch_result):
        pass


class TestWorldBatch:
    def test_empty_batch(self):
        world = World(10, 10)
        batch_in = WorldInput()
        batch_out = world.process(batch_in)
        assert isinstance(batch_out, WorldOutput)
        assert batch_out.is_empty()
