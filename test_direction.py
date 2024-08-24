from direction import Direction


class TestDirection:
    def test_hookup(self):
        assert 2 + 2 == 4

    def test_direction_EAST(self):
        dir = Direction.EAST

    def test_direction_left(self):
        east = Direction.EAST
        assert east.left() == Direction.NORTH

