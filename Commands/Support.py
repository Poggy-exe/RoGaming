from typing import Optional
from discord.utils import get
import discord
from discord.ext import commands
import json
import module
from src import guild_info


def syntax(command):
    aliases = "|".join([str(command), *command.aliases])
    params = []
    for key, value in command.params.items():
        if key not in ("self", "ctx"):
            params.append(f"[{key}]" if "NoneType" in str(
                value) else f"<{key}>")
    params = " ".join(params)

    return f"```{aliases} {params}```"


class Support(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="ticket")
    async def ticket(self, ctx, *, reason : str):
        
        case = module.ticket(ctx.author, reason)

        channel = await case.get_channel(ctx)      

        case.save()

        await channel.send(embed = case.get_embed(ctx))

    @commands.command()
    async def close(self,ctx,id : int):
        data = module.db("tickets").getDb()
        for i, t in enumerate(data["tickets"]):
            if t["id"] == id:
                data["tickets"].pop(i)
                module.db("tickets").saveDb(data)
                return
        await ctx.send("No such ticket exists0")

def setup(client):
    client.add_cog(Support(client))
