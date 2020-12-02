import discord
from discord.ext import commands
from discord.ext.commands import guild_only, has_permissions


class Moderation(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.bad_words = []

    @commands.command()
    async def whois(self, ctx, user: discord.Member):
        _embed = discord.Embed(color=discord.Color.from_rgb(
            254, 254, 254)).add_field(name="Id", value=user.id).add_field(name="Join date", value=user.joined_at.strftime("%d/%m/%Y %H:%M"))
        await ctx.send(embed=_embed)

    @commands.command()
    @guild_only()
    @has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int = 10):
        await ctx.message.delete()
        await ctx.channel.purge(limit=amount)
        await ctx.send(f"Cleared the last {amount} message(s)")

    @commands.command()
    @guild_only()
    @has_permissions(kick_members=True)
    async def kick(self, ctx, user : discord.Member, *, reason : str = "None provided"):
        await ctx.message.delete()
        await ctx.guild.kick(user, reason=reason)
        await ctx.send(f"{user} has been kicked for reason: `{reason}`")
        await user.send(f"You have been kicked from {ctx.guild} for reason: `{reason}`")

    @commands.command()
    @guild_only()
    @has_permissions(ban_members=True)
    async def ban(self, ctx, user : discord.Member, *, reason : str = "None provided"):
        await ctx.message.delete()
        await ctx.guild.ban(user, reason=reason)
        await ctx.send(f"{user} has been banned for reason: `{reason}`")
        await user.send(f"You have been banned from {ctx.guild} for reason: `{reason}`")

    @commands.command()
    @guild_only()
    @has_permissions(mute_members=True)
    async def mute(self, ctx, user : discord.Member, *, reason : str = "None provided"):
        await ctx.message.delete()
        await user.edit(mute=True)
        await ctx.send(f"{user} has been muted for reason: `{reason}`")

    @commands.command()
    @guild_only()
    @has_permissions(mute_members=True)
    async def unmute(self, ctx, user : discord.Member):
        await ctx.message.delete()
        await user.edit(mute=False)
        await ctx.send(f"{user} has been unmuted")

    @commands.command()
    @guild_only()
    @has_permissions(move_members=True)
    async def vc(self, ctx, user : discord.Member, channel : discord.VoiceChannel):
        await ctx.message.delete()
        await user.edit(voice_channel=channel)
        await ctx.send(f"{user} has been moved")

def setup(client):
    client.add_cog(Moderation(client))
