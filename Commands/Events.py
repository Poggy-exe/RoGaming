import discord
from discord.ext import commands
from discord.utils import get
import json

class Events(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_member_join(self,member):
        
        join_channel = get(member.guild.channels, name="joins│leaves")

        try:
            await join_channel.send(f"Welcome to RoGaming, {member.name}#{member.discriminator}. Play with us as we empower Gaming on the ROBLOX Platform.")
        except:
            print(f"User ({member.name}#{member.discriminator}) isn't accepting dm's")

        join_roles = ["RC Verified"]
        for role in join_roles:
            await member.add_roles(get(member.guild.roles, name=role), reason="Joined server!")
            
        with open("databases\\users.json", "r") as f:
            data = json.load(f)
            data["users"].append({"id":str(member.id),"links":[],"description":"No special description for this user","infractions":0})
        with open("databases\\users.json","w") as f:
            f.write(json.dumps(data))

    @commands.Cog.listener()
    async def on_member_leave(self,member):
        with open("databases\\users.json", "r") as f:
            data = json.load(f)
            index = -1
            for user in data["users"]:
                if user["id"] == str(member.id):
                    index = data["users"].index(user)
            data["users"].pop(index)
        with open("databases\\users.json","w") as f:
            f.write(json.dumps(data))


def setup(client):
    client.add_cog(Events(client))