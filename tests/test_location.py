from shared.direction import Direction
from shared.location import Location


class TestLocation:
    def test_location_plus_direction_math(self):
        location = Location(5, 5)
        assert location + Direction.NORTH == Location(5, 4)
        assert location + Direction.SOUTH == Location(5, 6)
        assert location + Direction.EAST == Location(6, 5)
        assert location + Direction.WEST == Location(4, 5)

    def test_location_add_returns_self_if_not_given_direction(self):
        location = Location(5, 5)
        assert location + location == location
