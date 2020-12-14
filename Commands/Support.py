from typing import Optional
from discord.utils import get
import discord
from discord.ext import commands
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
    async def close(self,ctx):

        id = await module.getTicketIdByChannelId(ctx.guild,ctx.message.channel.id)

        data = module.db("tickets").getDb()
        for i, t in enumerate(data["tickets"]):
            if t["id"] == id:
                data["tickets"].pop(i)
                module.db("tickets").saveDb(data)
                await ctx.send("Ticket closed")
                await ctx.message.channel.delete(reason="Ticket closed by moderator or user")

    @commands.command()
    async def claim(self,ctx, name = "claimed ticket"):
        try:
             id = await module.getTicketIdByChannelId(ctx.guild,ctx.message.channel.id)
            
            data = module.db("tickets").getDb()
            for i, t in enumerate(data["tickets"]):
                if t["id"] == id:
                    data["tickets"][i]["claimed"] = True
                    module.db("tickets").saveDb(data)
                    await ctx.message.channel.name = name + f" : {id}"
                    await ctx.send("Claimed") 

        except:
            await ctx.send("Must be in a ticket channel")
            return

def setup(client):
    client.add_cog(Support(client))
