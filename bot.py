import discord
from dotenv import dotenv_values
from database.database_manager import DatabaseManager
from game.room import Room
from game.player import Player
from game.command_handler import CommandHandler

# Load env values
config = dotenv_values('.env')
# Init discord
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# Init database
db_manager = DatabaseManager(config)

# Current game logic
room1 = Room("Starting Room", "You are in a dark room. There is a door to the north.")
room2 = Room("Bright Room", "You are in a bright room. There is a door to the south.")
room1.exits["north"] = room2
room2.exits["south"] = room1
players = {}

@client.event
async def on_ready():
    print('Bot is ready')

@client.event
async def on_message(message):
    # Ignore own messages
    if message.author == client.user:
        return
    # Get user id
    user_id = message.author.id
    player = None
    # Add user to players if not done yet
    if user_id not in players:
        players[user_id] = Player(message.author.name, room1)
        await message.channel.send(f"Welcome, {message.author.mention}! You have entered the MUD game. Type 'help' for a list of commands.")
    else:
        player = players[user_id]

    if player:
        words = message.content.split()
        if not words:
            return
        command = words[0].lower()
        args = words[1:]
        response = await CommandHandler(player, command, args).execute()
        await message.channel.send(f"{message.author.mention}, {response}")
    
client.run(config['DISCORD_TOKEN'])