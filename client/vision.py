from shared.location import Location


class Vision:
    def __init__(self, vision_list, location, direction):
        self.location = location
        self.direction = direction
        self.vision_list = vision_list

    def __iter__(self):
        return iter(self.vision_list)

    def __eq__(self, other):
        return self.location == (other.location
                 and self.direction == other.direction
                 and self.vision_list == other.vision_list)

    def match_forward_and_one_side(self, center, side):
        return self.forward_name() == center and (self.forward_left_name() == side or self.forward_right_name() == side)

    def forward_name(self):
        forward = self.location.forward(self.direction)
        return self.name_at(forward)

    def forward_left_name(self):
        forward_left = self.location.forward_left(self.direction)
        return self.name_at(forward_left)

    def forward_right_name(self):
        forward_right = self.location.forward_right(self.direction)
        return self.name_at(forward_right)

    def name_at(self, location: Location):
        return self._find_name_at(location.x, location.y)

    def _find_name_at(self, x, y):
        for name, vx, vy in self.vision_list:
            if vx == x and vy == y:
                return name
        return '_'
