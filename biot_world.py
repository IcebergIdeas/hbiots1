from entities import Entities
from point import Point


class BiotWorld:
    def __init__(self):
        self.biots = Entities()

    def add(self, biot):
        location = Point(10, 10)
        self.biots.place(biot, location)
        return {"location": location}
