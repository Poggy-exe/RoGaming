import discord
from discord.ext import commands
import requests

class Basic(commands.Cog):
    def __init__(self, client):
        self.client = client

    ## ____________ Commands ____________ ##
    
    # Ping Command
    @commands.command()
    async def ping(self, ctx):
        await ctx.send("Pong!")
      

    ## ____________ Events ____________ ##

    # On ready
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Bot is running as {self.client.user}")

def setup(client):
    client.add_cog(Basic(client))
