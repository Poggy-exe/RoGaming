import discord
from discord.ext import commands
from secrets import *
import os
import sys

sys.path.append(PATH_TO_LIBS)

client = commands.Bot(command_prefix=PREFIX)

commands = discord

for file in os.listdir("./Commands"):
    if file.endswith(".py"):
        print(f"Loaded : {file[:-3]} command(s)/event(s)")
        client.load_extension(f"Commands.{file[:-3]}")

client.run(TOKEN)