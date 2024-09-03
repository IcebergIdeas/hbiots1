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
            item = self.name_at(check_location.x, check_location.y)
            pattern_item = pattern[index]
            if pattern_item != '?' and pattern_item != item:
                return False
            index += 1
        return True

    def name_at(self, x, y=None):
        if isinstance(x, Location):
            return self.find_name_at(x.x, x.y)
        else:
            return self.find_name_at(x, y)

    def find_name_at(self, xx, yy):
        for name, vx, vy in self.vision_list:
            if vx == xx and vy == yy:
                return name
        return '_'


