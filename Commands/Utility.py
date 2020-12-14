import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, has_role, guild_only
from module import *
import re
import emoji

class Utility(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="cc",description="Create the channels")
    @has_permissions(manage_channels=True)
    @guild_only()
    async def create_channels(self, ctx, category: discord.CategoryChannel, name_format = "[game]",max_games: int = 20):
        max_games = min(max_games, 50)

        for channel in category.channels:
            await channel.delete()

        for game in games().getPopular(max_games)["games"]:
            name = re.sub(emoji.get_emoji_regexp(), r"", re.sub(r'\[.*?\]', "", game["name"])).strip().lower()
            print(name)
            name = name_format.replace("[game]", name)
            print(name)

            channel = await category.create_text_channel(name, overwrites={ctx.guild.default_role: discord.PermissionOverwrite(send_messages=False)})
            aliases = [name]            
            games().saveToDB(game["placeId"],game["name"], channel.id, aliases)

        for post in posts().getPosts():
            if(post["game_id"]):
                channel = discord.utils.get(
                    ctx.guild.channels, id=games().getChannelIdByGameId(post["game_id"]))
                user = self.client.get_user(post["user_id"])
                print(user)
                post_E = ad(post["description"], user, post["roblox_usr"],
                            post["game_id"], post["time"], post["reward"])
                await channel.send(embed=post_E.getEmbed())

    @commands.command(description="Add an alias for a channel for a game")
    @has_permissions(manage_channels=True)
    async def add_alias(self, ctx, channel: discord.TextChannel, *, alias):
        await ctx.send(embed=self.quickEmbed(games().addAliasWithChnId(channel, alias)))

    @commands.command(name="announce")
    @guild_only()
    async def send_message_as_embed(self,ctx, channel : discord.TextChannel, *, message : str):

        embed = discord.Embed(color=discord.Color.from_rgb(254,254,254), description=message)
        await channel.send(embed=embed)
        await ctx.message.delete()
    ## ____________ Events ____________ ##

    # Event
    # @commands.Cog.listener()


def setup(client):
    client.add_cog(Utility(client))