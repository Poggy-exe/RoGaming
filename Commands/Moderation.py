import discord
from typing import Optional
from discord.ext import commands
from discord.ext.commands import guild_only, has_permissions
from discord.utils import get
import module
from src.guild_info import *

class Moderation(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.bad_words = []

    @commands.command(name = "clear", description = "Deletes the last x amount of messages")
    @guild_only()
    @has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: Optional[int] = 10):
        await ctx.channel.purge(limit=amount)
        message = await ctx.send(f"Cleared the last {amount} messag")

    @commands.command(name = "kick", description = "Kicks a user from the server")
    @guild_only()
    @has_permissions(kick_members=True)
    async def kick(self, ctx, user : discord.Member, *, reason : Optional[str] = "None provided"):
        await ctx.guild.kick(user, reason=reason)
        await ctx.send(f"{user} has been kicked for reason: `{reason}`")
        await user.send(f"You have been kicked from {ctx.guild} for reason: `{reason}`")

    @commands.command(name = "ban", description = "Permanently bans a user from the server")
    @guild_only()
    @has_permissions(ban_members=True)
    async def ban(self, ctx, user : discord.Member, *, reason : Optional[str] = "None provided"):
        await ctx.guild.ban(user, reason=reason)
        await ctx.send(f"{user} has been banned for reason: `{reason}`")
        await user.send(f"You have been banned from {ctx.guild} for reason: `{reason}`")

    @commands.command(name = "mute", description = "Mutes a user from a vc")
    @guild_only()
    @has_permissions(manage_messages=True)
    async def mute(self, ctx, user : discord.Member, *, reason : Optional[str] = "None provided"):
        db = module.db("users")
        data = db.getDb()
        found_user = -1
        for i,db_user in enumerate(data["users"]):
            if db_user["id"] == user.id:
                found_user = i
                
        if found_user == -1:
            roles = []
            for role in user.roles:
                roles.append(role.id)
            data["users"].append({"id":str(user.id), "links":[], "description":[], "infractions":0, "roles":roles})
                
        db.saveDb(data)
        
        try:
            for owned_role in user.roles:
                if owned_role.name != "@everyone":
                    await user.remove_roles(owned_role, reason=reason)

            role = get(ctx.guild.roles, name="Muted")
            await user.add_roles(role, reason=reason)
        except:
            await ctx.send("User is already muted")
        await ctx.send(f"{user} has been muted for reason: `{reason}`")

    @commands.command(name = "unmute", description = "Unmutes a user from a vc")
    @guild_only()
    @has_permissions(manage_messages=True)
    async def unmute(self, ctx, user : discord.Member):
        db = module.db("users")
        data = db.getDb()
        found_user = -1
        for i,db_user in enumerate(data["users"]):
            if db_user["id"] == str(user.id):
                found_user = i
        if found_user == -1:
            await ctx.send("User is not in the database")
            return

        for role in data["users"][found_user]["roles"]:
            role = get(ctx.guild.roles, id = role)
            if role.name != "@everyone":
                await user.add_roles(role)

        
        role = get(ctx.guild.roles, name="Muted")
        try:
            await user.remove_roles(role)
        except:
            await ctx.send("User isn't muted")
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
