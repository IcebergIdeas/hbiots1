from direction import Direction
from point import Point


class Vision:
    def __init__(self, vision_list):
        self.vision_list = vision_list

    def matches(self, pattern, location: Point):
        index = 0
        for direction in Direction.EVERY:
            check_location = Point(direction.x, direction.y) + location
            item = self.vision_at(check_location.x, check_location.y)
            pattern_item = pattern[index]
            if pattern_item != '?' and pattern_item != item:
                return False
            index += 1
        return True

    def vision_at(self, x, y):
        for name, vx, vy in self.vision_list:
            if vx == x and vy == y:
                return name
        return '_'
