import discord
from discord.ext import commands
import string
import random
import requests
import custom_libs.db_interractions as db
import datetime


class Verification(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def verify(self, ctx, user):

        quickEmbed = lambda message: discord.Embed(description=message,color=discord.Color.from_rgb(254, 254, 254))

        r = requests.post("https://users.roblox.com/v1/usernames/users", {
            "usernames": [
                "JanuZz011"
            ],
            "excludeBannedUsers": True
        })
        data = r.json()
        if len(data["data"]) > 0:
          user_id = data["data"][0]["id"]
        else:
          await ctx.author.send(embed=quickEmbed("User was not found try again"))
          return

        verifyString = ''.join(random.choice(
        string.ascii_lowercase) for i in range(30))

        await ctx.author.send(embed=quickEmbed(f"Please put this `{verifyString}` in you status and reply to this message with your name to verify"))

        await self.client.wait_for("message", check=lambda context: context.author == ctx.author, timeout=300)

        r = requests.get(f"https://users.roblox.com/v1/users/{user_id}/status")
        if verifyString in r.json()["status"]:
          con = db.dbCon("dbs\\users.db")
          con.query("INSERT INTO TABLE Links VALUES('{}','{}','{}',{})".format(ctx.author.id, user_id, datetime.datetime.now().timestamp(),0,0))
          
          await ctx.author.send(embed=quickEmbed("roblox account has been linked"))


        else:
          await ctx.author.send(embed=quickEmbed("roblox account could not be linked"))


def setup(client):
    client.add_cog(Verification(client))
