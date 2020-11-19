import discord
from discord.ext import commands
import json
import requests
from datetime import datetime
from secrets import * 

class Advertising(commands.Cog):
    def __init__(self, client):
        self.client = client

        ## ____________ Variables ____________ ## 
        self.schema_path = "post_schemas\game-event.json"

        

    ## ____________ Commands ____________ ##

    # Command
    @commands.command()
    async def post(self, ctx):
        await ctx.send("Check your dm's a thread just started!")

        def Check(context):
            return context.author == ctx.author and isinstance(context.channel, discord.channel.DMChannel)

        def post(post : object):
            print(post)

        async def Ask(ctx, data : object, index : int, post : object, max_index : int,timeout :int = 60, check : callable = Check, next_ : callable = None):
            
            retry = lambda: Ask(ctx,data, index, post, max_index,timeout,check, next_)

            question = list(data["Questions"])[index]

            embed_q = discord.Embed(title = data["Title"], description=data["Description"])
            embed_q.add_field(name="Question", value=f"`{question['Question']}`")
            
            #print("Choises" in question)

            if("Example" in question):
                embed_q.add_field(name="Example",value= f'`{question["Example"] if "Example" in question else "None provided"}`')
                
            if("Choises" in question):
                embed_q.add_field(name="Choises",value=f'`{", ".join(question["Choises"]) if "Choises" in question else "Anything"}`')

            if("Format" in question):
                embed_q.add_field(name="Format",value=f'`{question["Format"] if "Format" in question else "Anything"}`')


            await ctx.author.send(embed=embed_q)
            
            try:
                answer = await self.client.wait_for("message", check=Check, timeout=60)
            except TimeoutError:
                await ctx.send("Thread closed due to timeout")
            
            value = answer.content

            if(question["Format"] == "Number"):
                try:
                    value = int(value)
                except ValueError:
                    await retry()
                if(value < 0):
                    await ctx.send("Must be a number (1,2,3... not 4.2 or 6.9)")
                    await retry()
            elif(question["Format"] == "Date"):
                try:
                    value = datetime.timestamp(datetime.strptime(value, "%H:%M %d/%m/%y"))
                    print(value)
                except ValueError:
                    await ctx.send("Must be a date in the format 'HH:MM dd/mm/yy'")
                    await retry()
            elif(question["Format"] == "Text"):
                try:
                    if(value.title() in question["Choises"]):
                        pass
                    else:
                        await ctx.send("Must be one of the given choises")
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
                data = r.json()
                if len(list(data["data"])) == 0:
                    await ctx.send("Must be a valid roblox user")
                    await retry()

            if(value == None):
                await retry()

            post[question["Name"]] = value

            if(index+1 <= max_index):
                await Ask(ctx, data, index+1, post, max_index, timeout, check, next_)
            else:
                if(next_):
                    next_(post)
                    
        
        try:
            with open(self.schema_path, "r") as f:
                data = json.loads(f.read())
                
                # Big boss didn't like this one
                await ctx.author.send("Hey! follow the steps below to start posting about your game")

                questions_len = len(list(data["Questions"]))

                start_index = 0

                try:
                    await Ask(ctx, data, start_index, {"Author":ctx.author.id}, questions_len-start_index-1, next_=post)
                except TimeoutError:
                    await ctx.author.send("Thread stopped it took too long")

        except FileNotFoundError:
            await ctx.send("The schema for this question could not be found. Please contact a Moderator and show them this message")


    ## ____________ Events ____________ ##

    # Event
    # @commands.Cog.listener()


def setup(client):
    client.add_cog(Advertising(client))