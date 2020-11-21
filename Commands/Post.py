import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, has_role
import json
import requests
from datetime import datetime
from secrets import *
import custom_module
import time


class Advertising(commands.Cog):
    def __init__(self, client):
        self.client = client

        ## ____________ Variables ____________ ##
        self.schema_path = "post_schemas\game-event.json"

    ## ____________ Commands ____________ ##

    # Command

    @commands.command()
    async def post(self, ctx):

        # The check to see if the message was sent in the right channel and/or by the same user as the origininal user
        def Check(context):
            return context.author == ctx.author and isinstance(context.channel, discord.channel.DMChannel)

        # The function where you have the information and you post it to the correct channel
        async def post(post: object):
                post_E = custom_module.post(post["Author"].id, post["Roblox username"],123123, post["Date"])
                await ctx.author.send(embed=post_E.getEmbed())

        async def Ask(ctx, data: object, index: int, post: object, max_index: int, timeout: int = 120, check: callable = Check, next_: callable = None):

            # a lambda for sending an embed wihout a title
            def quickEmbed(message): return discord.Embed(
                description=message, color=discord.Color.from_rgb(254, 254, 254))

            # lambda shortcut for retying the message if the user fails to give the correct informatiom
            def retry(): return Ask(ctx, data, index, post, max_index, timeout, check, next_)

            question = list(data["Questions"])[index]

            # The main embed where the question is asked
            embed_q = discord.Embed(title=data["Title"] if index == 0 else "", description=data["Description"]
                                    if index == 0 else "", color=discord.Color.from_rgb(254, 254, 254))

            #print("Choises" in question)

            # line break variable because you cant write it in f-strings
            br = "\n"

            embed_q.add_field(
                name=question['Question'], value=f'`{question["Example"] + br if "Example" in question else "None provided"}`', inline=False)

            if("Format" in question):
                embed_q.add_field(
                    name="Answer must be", value=f'`{question["Choises"] if "Choises" in question else question["Format"] if "Format" in question else "Anything"}`', inline=False)

            embed_q.add_field(
                name="\u200b", value="\nUse ``cancel`` to end this thread, it will end in 5 minutes.")

            await ctx.author.send(embed=embed_q)

            # Wait for the message that the user will respond with
            answer = await self.client.wait_for("message", check=Check, timeout=timeout)

            # DOESN'T WORK error check to see if the user took too long
            if answer == None:
                await ctx.author.send(embed=quickEmbed("Thread closed due to inactivity"))
                return

            value = answer.content

            # Check if the user cancelled the thread
            if(value.lower() == "cancel"):
                await ctx.author.send(embed=quickEmbed("Thread cancelled"))
                return
            else:
                # Check if there was any formatting associated with the question like number date or anything like that
                if(question["Format"] == "Number"):
                    try:
                        value = int(value)
                    except ValueError:
                        await retry()
                    if(value < 0):
                        await ctx.author.send(embed=quickEmbed("Must be a number (1,2,3... not 4.2 or 6.9)"))
                        await retry()
                elif(question["Format"] == "Game"):
                    if value.lower() not in data["Games"]:
                        await ctx.author.send(embed=quickEmbed("""

                            Input Error

                            You're reply was not a valid response to your options.
                            Please give a valid input, e.g. ``Bloxburg``

                            """))

                        await retry()
                elif(question["Format"] == "Date"):
                    try:
                        currTime = datetime.now()
                        timestamp = datetime.strptime(value + " {}/{}/{}".format(currTime.day, currTime.month,currTime.year), "%H:%M %d/%m/%Y").timestamp()
                        if(timestamp < currTime.timestamp()):
                            await ctx.author.send(embed=quickEmbed(f"It has already been {value} please pick a time that has not been"))
                            await retry()
                        value = timestamp
                    except ValueError:
                        await ctx.author.send(embed=quickEmbed("Must be a date in the format `HH:MM`"))
                        await retry()
                elif(question["Format"] == "Text"):
                    try:
                        if(value.title() in question["Choises"]):
                            pass
                        else:
                            await ctx.author.send(embed=quickEmbed("Must be one of the given choises"))
                            await retry()
                    except KeyError:
                        pass
                elif(question["Format"] == "User"):

                    # Ask the roblox api if the user exists
                    body_ = {
                        "usernames": [
                            value
                        ],
                        "excludeBannedUsers": True
                    }
                    r = requests.post(
                        "https://users.roblox.com/v1/usernames/users", data=body_)
                    resp = r.json()
                    if(r.status_code != 200):
                        await ctx.author.send(embed=quickEmbed(f"Internal server error: {r.status_code}\nPlease try again later"))
                        return
                    if len(list(resp["data"])) == 0:
                        await ctx.author.send(embed=quickEmbed("Roblox user not found? Did you type the name correctly?"))
                        await retry()

                if(value == None):
                    await retry()

                post[question["Name"]] = value

                # If there are more questions do those otherwise return the collected information
                if(index+1 <= max_index):
                    await Ask(ctx, data, index+1, post, max_index, timeout, check, next_)
                else:
                    if(next_):
                        await next_(post)
                    return post

        try:
            with open(self.schema_path, "r") as f:
                data = json.loads(f.read())

                questions_len = len(list(data["Questions"]))

                start_index = 0

                await Ask(ctx, data, start_index, {"Author": ctx.author}, questions_len-start_index-1, next_=post)

        except FileNotFoundError:
            await ctx.author.send("The schema for this question could not be found. Please contact a Moderator and show them this message")

    @commands.command()
    @has_permissions(manage_channels=True)
    async def cc(self, ctx, category: discord.CategoryChannel, max_games: int = 20):

        for channel in category.channels:
            await channel.delete()

        # for game in games().getPopular(max_games)["games"]:
        #     name = game["name"]
        #     channel = await category.create_text_channel(name, overwrites={ctx.guild.default_role: discord.PermissionOverwrite(send_messages=False)})

    ## ____________ Events ____________ ##

    # Event
    # @commands.Cog.listener()


def setup(client):
    client.add_cog(Advertising(client))
