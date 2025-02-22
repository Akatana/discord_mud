class CommandHandler:
    def __init__(self, player, command, args):
        self.player = player
        self.command = command
        self.args = args

    async def execute(self):
        match self.command:
            case 'look' | 'l':
                return await self.look()
            case 'north' | 'n' | 'east' | 'e' | 'south' | 's' | 'west' | 'w':
                return await self.go(self.command[0])
            case 'take':
                return await self.take(self.args[0] if self.args else None)
            case 'inv' | 'inventory':
                return await self.inventory()
            case _:
                return "Unknown command. Try 'look', '[direction]', 'take [item]', or 'inventory'."

    async def look(self):
        room = self.player.current_room
        response = room.description
        if room.items:
            response += "\nItems: " + ", ".join(item.name for item in room.items)
        if room.exits:
            response += "\nExits: " + ", ".join(room.exits.keys())
        return response
    
    async def go(self, direction):
        room = self.player.current_room
        for exit in room.exits:
            if direction == exit[0]:
                new_room = room.exits[exit]
                self.player.current_room = new_room
                response = f"You go {exit} and enter {new_room.name}."
                response += "\n" + await self.look()
                return response
        response = f"There is no exit to the {direction}."
        return response
    
    async def take(self, item_name):
        room = self.player.current_room
        for item in room.items:
            if item.name.lower() == item_name.lower():
                self.player.inventory.append(item)
                room.items.remove(item)
                response = f"You take {item.name}."
                return response
        response = f"There is no {item_name} here."
        return response
    
    async def inventory(self):
        if self.player.inventory:
            response = "You are carrying: " + ", ".join(item.name for item in self.player.inventory)
        else:
            response = "You are not carrying any items."
        return response