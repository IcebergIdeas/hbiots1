class Entities:
    def __init__(self):
        self.contents = {}

    def place(self, biot, location):
        self.contents[location] = biot
