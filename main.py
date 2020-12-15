import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
from secrets import *
import os
import sys

client = commands.Bot(command_prefix=".")

client.remove_command("help")

for file in os.listdir("./Commands"):
    if file.endswith(".py"):
        print(f"Loaded : {file[:-3]} command(s)/event(s)")
        client.load_extension(f"Commands.{file[:-3]}")

@client.event
async def on_ready():
    print(f"Bot is running as {client.user}")

client.run(TOKEN)