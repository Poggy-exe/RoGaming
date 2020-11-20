import discord
from discord.ext import commands
import json
import requests
from datetime import datetime
from secrets import * 
#from random import randint

class Advertising(commands.Cog):
    def __init__(self, client):
        self.client = client

        ## ____________ Variables ____________ ## 
        self.schema_path = "post_schemas\game-event.json"

        

    ## ____________ Commands ____________ ##

    # Command
    @commands.command()
    async def post(self, ctx):

        def Check(context):
            return context.author == ctx.author and isinstance(context.channel, discord.channel.DMChannel)

        def post(post : object):
            print(post)

        async def Ask(ctx, data : object, index : int, post : object, max_index : int,timeout : int = 120, check : callable = Check, next_ : callable = None):
            
            retry = lambda: Ask(ctx,data, index, post, max_index,timeout,check, next_)

            question = list(data["Questions"])[index]

            embed_q = discord.Embed(title = data["Title"] if index == 0 else "", description=data["Description"] if index == 0 else "", color=discord.Color.from_rgb(253,253,253))

            #print("Choises" in question)

            br = "\n"

            embed_q.add_field(name=question['Question'],value= f'`{question["Example"] + br if "Example" in question else "None provided"}`', inline=False)
                
            if("Format" in question):
                embed_q.add_field(name="Answer must be",value=f'`{question["Format"] if "Format" in question else "Anything"}`', inline=False)

            embed_q.add_field(name="\u200b", value="\nUse `cancel` to cancel thread")

            await ctx.author.send(embed=embed_q)
            
            answer = await self.client.wait_for("message", check=Check, timeout=timeout)
            
            if answer == None:
                await ctx.author.send("Thread closed due to inactivity")
                return
            
            value = answer.content

            if(value.lower() == "cancel"):
                await ctx.author.send("Thread cancelled")
                return

            if(question["Format"] == "Number"):
                try:
                    value = int(value)
                except ValueError:
                    await retry()
                if(value < 0):
                    await ctx.author.send("Must be a number (1,2,3... not 4.2 or 6.9)")
                    await retry()
            elif(question["Format"] == "Date"):
                try:
                    value = datetime.timestamp(datetime.strptime(value, "%H:%M %d/%m/%y"))
                    print(value)
                except ValueError:
                    await ctx.author.send("Must be a date in the format 'HH:MM dd/mm/yy'")
                    await retry()
            elif(question["Format"] == "Text"):
                try:
                    if(value.title() in question["Choises"]):
                        pass
                    else:
                        await ctx.author.send("Must be one of the given choises")
                        await retry()
                except KeyError:
                    pass  
            elif(question["Format"] == "User"):
                body_ = {
                  "usernames": [
                    value
                  ],
                  "excludeBannedUsers": True
                }
                r = requests.post("https://users.roblox.com/v1/usernames/users", data=body_)
                resp = r.json()
                if(r.status_code != 200):
                    await ctx.author.send(f"Internal server error: {r.status_code}\nPlease try again later")
                    return
                if len(list(resp["data"])) == 0:
                    await ctx.author.send("Must be a valid roblox user")
                    print
                    await retry()

            if(value == None):
                await retry()

            post[question["Name"]] = value

            if(index+1 <= max_index):
                await Ask(ctx, data, index+1, post, max_index, timeout, check, next_)
            else:
                if(next_):
                    next_(post)
                return post
                    
        
        try:
            with open(self.schema_path, "r") as f:
                data = json.loads(f.read())
                
                questions_len = len(list(data["Questions"]))

                start_index = 0

                try:
                    await Ask(ctx, data, start_index, {"Author":ctx.author.id}, questions_len-start_index-1, next_=post)
                except TimeoutError:
                    await ctx.author.send("Thread stopped it took too long")

        except FileNotFoundError:
            await ctx.author.send("The schema for this question could not be found. Please contact a Moderator and show them this message")


    ## ____________ Events ____________ ##

    # Event
    # @commands.Cog.listener()


def setup(client):
    client.add_cog(Advertising(client))
