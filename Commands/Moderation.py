import discord
from typing import Optional
from discord.ext import commands
from discord.ext.commands import guild_only
from discord.ext.commands import has_permissions
import module

class Moderation(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.bad_words = []

    @commands.command(name = "clear", description = "Deletes the last x amount of messages")
    @guild_only()
    @has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: Optional[int] = 10):
        #await ctx.message.delete()
        await ctx.channel.purge(limit=amount)
        message = await ctx.send(f"Cleared the last {amount} message(s)")
        message.delete()

    @commands.command(name = "kick", description = "Kicks a user from the server")
    @guild_only()
    @has_permissions(kick_members=True)
    async def kick(self, ctx, user : discord.Member, *, reason : Optional[str] = "None provided"):
        await ctx.message.delete()
        await ctx.guild.kick(user, reason=reason)
        await ctx.send(f"{user} has been kicked for reason: `{reason}`")
        await user.send(f"You have been kicked from {ctx.guild} for reason: `{reason}`")

    @commands.command(name = "ban", description = "Permanently bans a user from the server")
    @guild_only()
    @has_permissions(ban_members=True)
    async def ban(self, ctx, user : discord.Member, *, reason : Optional[str] = "None provided"):
        await ctx.message.delete()
        await ctx.guild.ban(user, reason=reason)
        await ctx.send(f"{user} has been banned for reason: `{reason}`")
        await user.send(f"You have been banned from {ctx.guild} for reason: `{reason}`")

    @commands.command(name = "mute", description = "Mutes a user from a vc")
    @guild_only()
    @has_permissions(manage_messages=True)
    async def mute(self, ctx, user : discord.Member, *, reason : Optional[str] = "None provided"):
        await ctx.message.delete()
        await user.edit(mute=True)
        await ctx.send(f"{user} has been muted for reason: `{reason}`")

    @commands.command(name = "unmute", description = "Unmutes a user from a vc")
    @guild_only()
    @has_permissions(manage_messages=True)
    async def unmute(self, ctx, user : discord.Member):
        await ctx.message.delete()
        await user.edit(mute=False)
        await ctx.send(f"{user} has been unmuted")

    @commands.command(name="describe")
    @has_permissions(manage_roles=True)
    async def set_usr_description(self, ctx, user : discord.Member, *, desc):
        module.user(str(user.id)).setDescription(desc)
        await ctx.send("Description updated")

    @commands.command(name="set_infractions")
    @has_permissions(manage_roles=True)
    async def set_infractions(self, ctx, user : discord.Member, n):
        module.user(str(user.id)).setInfractions(n)
        await ctx.send("Infractions updated")

def setup(client):
    client.add_cog(Moderation(client))
