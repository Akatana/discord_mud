class Room:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.exits = {}  # Dictionary of directions and connected rooms
        self.items = []  # List of items in the room