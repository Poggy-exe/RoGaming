from typing import Optional
from discord.utils import get
import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
import json
import module
from src import guild_info

class Support(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="ticket")
    async def ticket(self, ctx, *, reason : str):
        
        case = module.ticket(ctx.author, reason)

        channel = await case.get_channel(ctx)      

        case.save()

        msg = await channel.send(embed = case.get_embed(ctx))

        await msg.pin()

    @commands.command()
    @has_permissions(manage_channels=True)
    async def close(self,ctx,*,reason = "None provided"):

        id = await module.getTicketIdByChannelId(ctx.guild,ctx.message.channel.id)

        data = module.db("tickets").getDb()
        for i, t in enumerate(data["tickets"]):
            if t["id"] == id:
                data["tickets"][i]["close-reason"] = reason
                module.db("tickets").saveDb(data)
                await ctx.send("Ticket closed")
                await ctx.message.channel.delete(reason="Ticket closed by moderator or user")

    @commands.command()
    @has_permissions(manage_channels=True)
    async def claim(self,ctx, *,name = "claimed ticket"):
        print(name.replace(" ","-"))
        try:
            id = await module.getTicketIdByChannelId(ctx.guild,ctx.message.channel.id)

            data = module.db("tickets").getDb()
            for i, t in enumerate(data["tickets"]):
                if t["id"] == id:
                    if(t["claimed"] == False):
                        data["tickets"][i]["claimed"] = True
                        module.db("tickets").saveDb(data)
                        await ctx.message.channel.edit(name = name + f" {id}")
                        await ctx.send("Claimed")
                    else:
                        await ctx.send("Already claimed")

        except:
            await ctx.send("Must be in a ticket channel")
            return

def setup(client):
    client.add_cog(Support(client))
