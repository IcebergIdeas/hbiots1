import pytest

from shared.direction import Direction


class TestDirection:
    def test_direction_left(self):
        east = Direction.EAST
        assert east.left() == Direction.NORTH

    def test_direction_right(self):
        east = Direction.EAST
        assert east.right() == Direction.SOUTH

    def test_cannot_remove_from_all(self):
        with pytest.raises(AttributeError):
            Direction.ALL.remove(Direction.NORTH)

    def test_cannot_remove_from_every(self):
        with pytest.raises(AttributeError):
            Direction.EVERY.remove(Direction.NORTH)
