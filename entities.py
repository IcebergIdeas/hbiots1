from point import Point


class Entities:
    def __init__(self):
        self.contents = {}

    def place(self, biot):
        self.contents[biot.id] = biot

    def entity_at(self, column, row):
        point = Point(column, row)
        for entity in self.contents.values():
            if entity.location == point:
                return entity
        return None
