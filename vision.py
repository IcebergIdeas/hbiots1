from typing import Union

from direction import Direction
from location import Location


class Vision:
    def __init__(self, vision_list):
        self.vision_list = vision_list

    def __iter__(self):
        return iter(self.vision_list)

    def matches(self, pattern, location: Location):
        index = 0
        for direction in Direction.EVERY:
            check_location = location + direction
            item = self.name_at(check_location)
            pattern_item = pattern[index]
            if pattern_item != '?' and pattern_item != item:
                return False
            index += 1
        return True

    def name_at(self, location: Location):
        return self._find_name_at(location.x, location.y)

    def _find_name_at(self, x, y):
        for name, vx, vy in self.vision_list:
            if vx == x and vy == y:
                return name
        return '_'


