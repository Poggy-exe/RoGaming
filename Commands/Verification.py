import discord
from discord.ext import commands
import string
import random

class Verification(discord.Cog):
  def __init__(self, client):
    self.client = client
    
  @commands.command()
  async def verify(self, ctx):
    quickEmbed = lambda message: discord.Embed(color=discord.Color.from_rgb(254,254,254)).add_field(name="\u200b",value=message)
    verifyString = ''.join(random.choice(string.ascii_lowercase) for i in range(30))
    
    await ctx.author.send(embed=quickEmbed(f"Please put this `{verifyString}` in you status and reply to this message with your name to verify"))
    
    ctx.author.send(embed=quickEmbed(""))

def setup(client):
  client.add_cog(Verification(client))
