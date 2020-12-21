import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, has_role, guild_only
from discord.utils import get
from module import *
import re
import emoji

class Utility(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def link_game(self, ctx, channel_id : discord.TextChannel, game_id : int, *,game_name : str):
        games().linkGame(channel_id.id, game_name, game_id, ctx.guild.id)
        await ctx.send("Game linked!")
        # except:
        #     await ctx.send("Could not link game")

def setup(client):
    client.add_cog(Utility(client))