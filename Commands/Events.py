import discord
from discord.ext import commands
from discord.utils import get
import json

class Events(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    join_roles = ["RC Verified"]
    
    @commands.Cog.listener()
    async def on_member_join(self,member):
        
        for role in join_roles:
            try:
                role = get(member.server.roles, name=role)
                await self.client.add_roles(member, role)

        member.add
        with open("databases\\users.json", "r") as f:
            data = json.load(f.read())
            data["users"].append({"id":str(member.id),"links":[],"description":"No special description for this user","infractions":0})
        with open("databases\\users.json","w") as f:
            f.write(json.dumps(data))

    @commands.Cog.listener()
    async def on_member_leave(self,member):
        with open("databases\\users.json", "r") as f:
            data = json.load(f.read())
            index = -1
            for user in data["users"]:
                if user["id"] == str(member.id):
                    index = data["users"].index(user)
            data["users"].pop(index)
        with open("databases\\users.json","w") as f:
            f.write(json.dumps(data))


def setup(client):
    client.add_cog(Events(client))