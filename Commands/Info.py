from typing import Optional
from discord.utils import get
import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
import json
import module


def syntax(command):
    aliases = "|".join([str(command), *command.aliases])
    params = []
    for key, value in command.params.items():
        if key not in ("self", "ctx"):
            params.append(f"[{key}]" if "NoneType" in str(
                value) else f"<{key}>")
    params = " ".join(params)

    return f"```{aliases} {params}```"


class Info(commands.Cog):
    def __init__(self, client):
        self.client = client

    async def cmd_help(self, ctx, command):
        embed = discord.Embed(title=f"Help for `command`", color=discord.Color.from_rgb(
            254, 254, 254), description=syntax(command))
        embed.add_field(name="Command description", value=command.help)
        await ctx.send(embed=embed)

    @commands.command(name="help")
    async def show_help(self, ctx, cmd: Optional[str]):
        """Shows this message"""
        if cmd is None:
            embed = discord.Embed(color=discord.Color.from_rgb(
                254, 254, 254), title="Help Command", description="These following commands for this bot.")
            for cog in self.client.cogs:
                commandLst = ""
                for command in self.client.get_cog(cog).walk_commands():
                    commandLst += f"`{str(command.name)}`\n"
                if(commandLst.strip() != ""):
                    embed.add_field(name=f"**{cog}**",
                                    value=commandLst, inline=False)
            await ctx.send(embed=embed)
        else:
            if(get(self.client.commands, name=cmd)):
                command = get(self.client.commands, name=cmd)
                await self.cmd_help(ctx, command)
            else:
                await ctx.send("Command not found")

    @commands.command(name="getId")
    async def getId(self, ctx, user: discord.Member):
        _embed = discord.Embed(color=discord.Color.from_rgb(
            254, 254, 254)).add_field(name="Id", value=user.id)
        await ctx.send(embed=_embed)

    @commands.command()
    async def records(self, ctx, user: discord.Member):
        userJson = {}

        users = module.db("users").getDb()["users"]
        for dbUser in users:
            if dbUser["id"] == str(user.id):
                userJson = dbUser

        if userJson == {}:
            print("No user found")
            userJson = {"id": str(
                ctx.author.id), "description": "No special info about user", "links": [], "infractions": 0}

        embed = discord.Embed(color=discord.Color.from_rgb(254, 254, 254), title=f"{user.name}#{user.discriminator}", description=userJson["description"]+"\n",)
        embed.add_field(name="Infractions", value=str(userJson["infractions"]))

        smString = ""

        for sm in userJson["links"]:
            data = module.db("socialMedias").getDb()
            index = list(data["emojis"].keys()).index(list(sm.keys())[0])
            emoji = list(data["emojis"].values())[index]
            smString += f"{emoji}{list(sm.values())[0]}\n"

        if smString != "":
            embed.add_field(name="Social Media", value=smString, inline=False)

        embed.set_thumbnail(url=user.avatar_url)

        await ctx.send(embed=embed)

    @commands.command(name="link")
    async def link_social_media(self, ctx, media, name):

        data = module.db("socialMedias").getDb()
        if media.lower() not in data["emojis"].keys():
            await ctx.send("That social media is not allowed to be linked")
            return

        link = {media.lower(): name}

        users = module.db("users").getDb()["users"]

        userInDb = False

        for user in users:
            if user["id"] == str(ctx.author.id):
                userInDb = True

        if not userInDb:
            users.append({"id": str(ctx.author.id), "links": [],"description":"No special description for this user","infractions":0})

        for user in users:
            if str(user["id"]) == str(ctx.author.id):
                if(link in user["links"]):
                    user["links"].pop(user["links"].index(link))
                    await ctx.send("Removed link")
                else:
                    try:
                        user["links"].append(link)
                    except:
                        user["links"] = [link]
                    break
                    await ctx.send("Added link")

        module.db("users").saveDb({"users":users})


def setup(client):
    client.add_cog(Info(client))
