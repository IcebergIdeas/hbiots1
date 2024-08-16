class Entities:
    def __init__(self):
        self.contents = {}

    def place(self, biot):
        self.contents[biot.id] = biot
