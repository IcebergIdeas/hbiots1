from entities import Entities
from point import Point


class World:
    def __init__(self):
        self.biots = Entities()

    def add(self, biot):
        location = Point(10, 10)
        biot.id = 101
        biot.location = location
        self.biots.place(biot)

    def move(self, biot, dx, dy):
        biot = self.biots.contents[biot.id]
        location = biot.location
        biot.location = Point(location.x + dx, location.y + dy)