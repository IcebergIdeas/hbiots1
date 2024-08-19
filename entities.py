from point import Point


class Entities:
    def __init__(self):
        self.contents = {}

    def place(self, biot):
        self.contents[biot.id] = biot

    def entity_at(self, x, y):
        point = Point(x, y)
        for entity in self.contents.values():
            if entity.location == point:
                return entity
        return None

    def __eq__(self, other):
        his_contents = other.get_entities()
        if not self.check_all_his_things_are_valid(his_contents):
            return False
        print( len(self.contents), len(his_contents))
        return len(self.contents) == len(his_contents)

    def check_all_his_things_are_valid(self, his_contents):
        what_he_has_is_correct = True
        for map_dict in his_contents:
            his_x = map_dict.x
            his_y = map_dict.y
            his_name = map_dict.name
            if self.entity_at(his_x, his_y).name != his_name:
                what_he_has_is_correct = False
        print(f"returning {what_he_has_is_correct}")
        return what_he_has_is_correct


