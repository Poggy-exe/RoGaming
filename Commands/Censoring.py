import discord
from discord.ext import commands
import module

class Filters(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.bad_words = []

    @commands.Cog.listener()
    async def on_message(self,msg):
        with open("src/bad-words.txt", "r") as f:
            self.bad_words = f.read().splitlines()
        for word in self.bad_words:
            if word.lower() in msg.content.lower():
                module.user(str(msg.author.id)).addInfraction()
                await msg.delete()
                await msg.channel.send(f"{msg.author.mention}, please don't use inappropriate language")
        #await self.client.process_commands(msg)
    
    @commands.command()
    async def blacklist(self, ctx, word : str):
        with open("src/bad-words.txt", "a+") as f:
            f.write(word + "\n")

    @commands.command()
    async def whitelist(self, ctx, word : str):
        words = []
        with open("src/bad-words.txt", "r") as f:
            words = f.read().splitlines()
        if word.lower() in words:
            words.pop(words.index(word))
            with open("src/bad-words.txt", "w") as f:
                f.write("\n".join(words))

def setup(client):
    client.add_cog(Filters(client))