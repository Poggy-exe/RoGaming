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

    
    @commands.command()
    async def whois(self,ctx, user : discord.Member):
        _embed = discord.Embed(color=discord.Color.from_rgb(254,254,254)).add_field(name="id", value=user.id)
        await ctx.send(embed=_embed)
        

    ## ____________ Events ____________ ##

    # On ready
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Bot is running as {self.client.user}")

def setup(client):
    client.add_cog(Basic(client))
