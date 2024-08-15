class Entities:
    def __init__(self):
        self.contents = {}

    def place(self, biot_id, world_biot):
        self.contents[biot_id] = world_biot
