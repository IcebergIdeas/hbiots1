from typing import Union

from direction import Direction
from location import Location


class Vision:
    def __init__(self, vision_list):
        self.vision_list = vision_list

    def __iter__(self):
        return iter(self.vision_list)

    def name_at(self, location: Location):
        return self._find_name_at(location.x, location.y)

    def _find_name_at(self, x, y):
        for name, vx, vy in self.vision_list:
            if vx == x and vy == y:
                return name
        return '_'
