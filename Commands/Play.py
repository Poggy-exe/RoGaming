import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, has_role, guild_only
import json
import requests
from datetime import *
from secrets import *
from module import *
import emoji
import re
import time
from pytz import timezone


class Post(commands.Cog):
    def __init__(self, client):
        self.client = client

        ## ____________ Variables ____________ ##
        self.schema_path = "post_schemas\game-event.json"

        # a lambda for sending an embed wihout a title
        self.quickEmbed = lambda message: discord.Embed(
            description=message, color=discord.Color.from_rgb(254, 254, 254))

    ## ____________ Commands ____________ ##

    # Command

    @commands.command(name = "play", description = "Start a thread to post you game invite")
    @guild_only()
    async def play(self, ctx):

        # The check to see if the message was sent in the right channel and/or by the same user as the origininal user
        def Check(context):
            return context.author == ctx.author and isinstance(context.channel, discord.channel.DMChannel)

        # The function where you have the information and you post it to the correct channel
        async def post(post: object):
            post_ad = ad(post["Info"], post["Author"], post["Roblox username"],
                         post["Game"], post["Date"], post["Reward"])

            c_id = games().getChannelIdByGameId(post["Game"])

            channel = discord.utils.get(ctx.guild.channels, id=c_id)

            post_ad.saveToDB()

            await channel.send(embed=post_ad.getEmbed())

            print("Question posted")


        async def Ask(ctx, data: object, index: int, post: object, max_index: int, timeout: int = 120, check: callable = Check, next_: callable = None):

            # lambda shortcut for retying the message if the user fails to give the correct informatiom
            def retry(): return Ask(ctx, data, index, post, max_index, timeout, check, next_)

            question = list(data["Questions"])[index]

            # The main embed where the question is asked
            embed_q = discord.Embed(title=data["Title"] if index == 0 else "", description=data["Description"]
                                    if index == 0 else "", color=discord.Color.from_rgb(254, 254, 254))

            # line break variable because you cant write it in f-strings
            br = "\n"

            embed_q.add_field(
                name=question['Question'], value=f'\n> {question["Example"] + br if "Example" in question else "None provided"}', inline=False)

            # if("Format" in question):
            #     embed_q.add_field(
            #         name="Answer must be", value=f'`{question["Choises"] if "Choises" in question else question["Format"] if "Format" in question else "Anything"}`', inline=False)

            embed_q.add_field(
                name="\u200b", value="\nUse ``cancel`` to end this thread, you have 5 minutes to answer this question.")

            await ctx.author.send(embed=embed_q)

            # Wait for the message that the user will respond with
            answer = await self.client.wait_for("message", check=Check, timeout=timeout)

            # DOESN'T WORK error check to see if the user took too long
            if answer == None:
                await ctx.author.send(embed=self.quickEmbed("Thread closed due to inactivity"))
                return

            value = answer.content

            # Check if the user cancelled the thread
            if(value.lower() == "cancel"):
                await ctx.author.send(embed=self.quickEmbed("Thread cancelled"))
                return
            else:
                # Check if there was any formatting associated with the question like number date or anything like that
                if(question["Format"] == "Number"):
                    try:
                        value = int(value)
                        if(value < 0):
                            await ctx.author.send(embed=self.quickEmbed("Must be a number (1,2,3... not 4.2 or 6.9)"))
                            await retry()
                    except ValueError:
                        await retry()

                elif(question["Format"] == "Game"):
                    game_id = games().getIdByName(value)
                    if game_id == -1:
                        await ctx.author.send(embed=self.quickEmbed("""

                            Input Error

                            You're reply was not a valid response to your options.
                            Please give a valid input, e.g. ``Bloxburg``

                            """))

                        await retry()
                    value = game_id
                elif(question["Format"] == "Date"):
                    try:
                        curr_time = datetime.utcnow()
                        time_str = value + \
                            curr_time.strftime(" %d/%m/%Y") + " UTC"
                        time_ob = datetime.strptime(
                            time_str, "%H:%M %d/%m/%Y %Z")
                        print(time_ob.timestamp())
                        if curr_time.timestamp() < time_ob.timestamp():
                            value = time_ob.timestamp()
                        else:
                            await ctx.author.send(embed=self.quickEmbed(f"It has already been {value} please choose a time that has not been. Later than {curr_time.hour}:{curr_time.minute}"))
                            await retry()
                    except:
                        await ctx.author.send(embed=self.quickEmbed("Must be time in format HH:MM"))
                        await retry()
                elif(question["Format"] == "Text"):
                    try:
                        if(value.title() in question["Choises"]):
                            pass
                        else:
                            await ctx.author.send(embed=self.quickEmbed("Must be one of the given choises"))
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
                        await ctx.author.send(embed=self.quickEmbed(f"Internal server error: {r.status_code}\nPlease try again later"))
                        return
                    if len(list(resp["data"])) == 0:
                        await ctx.author.send(embed=self.quickEmbed("Roblox user not found? Did you type the name correctly?"))
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
                    return
                return

        try:
            with open(self.schema_path, "r") as f:
                data = json.loads(f.read())

                questions_len = len(list(data["Questions"]))

                start_index = 0

                await Ask(ctx, data, start_index, {"Author": ctx.author}, questions_len-start_index-1, next_=post)

                return
        except FileNotFoundError:
            await ctx.author.send("The schema for this question could not be found. Please contact a Moderator and show them this message")

def setup(client):
    client.add_cog(Post(client))