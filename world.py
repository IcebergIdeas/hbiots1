from biot import Biot
from entities import Entities
from point import Point


class WorldBiot:
    def __init__(self, id, location):
        self.id = id
        self.location = location


class World:
    def __init__(self):
        self.biots = Entities()

    def add(self, biot):
        id = 101
        location = Point(10, 10)
        biot.id = id
        biot.location = location
        self.biots.place(id, biot)

    def move(self, biot_id, dx, dy):
        world_biot = self.biots.contents[biot_id]
        location = world_biot.location
        world_biot.location = Point(location.x + dx, location.y + dy)
        return {"ID": biot_id, "location": world_biot.location}
