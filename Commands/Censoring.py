import discord
from discord.ext import commands

class Censoring(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.bad_words = []

    @commands.Cog.listener()
    async def on_message(self,msg):
        with open("src/bad-words.txt", "r") as f:
            self.bad_words = f.read().splitlines()
        for word in self.bad_words:
            if word.lower() in msg.content.lower():
                await msg.delete()
                await msg.channel.send(f"{msg.author.mention}, please don't use inappropriate language")
        #await self.client.process_commands(msg)

def setup(client):
    client.add_cog(Censoring(client))