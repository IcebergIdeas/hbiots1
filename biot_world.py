from entities import Entities
from point import Point


class BiotWorld:
    def __init__(self):
        self.biots = Entities()

    def add(self, biot):
        location = Point(10, 10)
        self.biots.place(biot, location)
        return {"location": location}

    def move(self, biot, dx, dy):
        biot = self.biots.contents[biot]
        location = biot.location
        new_location = Point(location.x + dx, location.y + dy)
        self.biots.place(biot, new_location)
