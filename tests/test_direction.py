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

    def test_from_name(self):
        assert Direction.from_name('WEST') == Direction.WEST
        assert Direction.from_name('NORTH') == Direction.NORTH
        assert Direction.from_name('EAST') == Direction.EAST
        assert Direction.from_name('SOUTH') == Direction.SOUTH
        assert Direction.from_name('fred') == Direction.EAST
