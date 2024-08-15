class Entities:
    def __init__(self):
        self.contents = {}

    def place(self, biot, location):
        biot.location = location
        self.contents[biot] = biot
