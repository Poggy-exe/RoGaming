import discord
import requests
from datetime import * 
import json

class games():
    def getSorts(self):
        r = requests.get("https://games.roblox.com/v1/games/sorts")
        return r.json()

    def getList(self, sortToken: str, Max_rows: int = 20):
        r = requests.get(
            f"https://games.roblox.com/v1/games/list?model.sortToken={sortToken}&model.maxRows={Max_rows}")
        return r.json()

    def getPopular(self, Max_rows: int = 20):
        sorts = self.getSorts()["sorts"]
        token = ""
        for sort in sorts:
            if(sort["name"] == "Popular"):
                token = sort["token"]
        games_list = self.getList(token, Max_rows)
        return games_list

    def getIdByName(self, name : str):
        with open("databases\\game.json", "r") as f:
            data = json.loads(f.read())

            id = -1

            for game in data["games"]:
                if(name.lower() in game["aliases"]):
                    id = game["id"]

            return id

    def getImgUrlById(self, id):
        url = f"https://thumbnails.roblox.com/v1/assets?assetIds={id}&size=768x432&format=Png&isCircular=false"
        r = requests.get(url)
        data = r.json()
        print(data)
        try:
            return data["data"][0]["imageUrl"]
        except:
            return ""

    def getNameById(self,id):
        with open("databases\\game.json", "r") as f:
            data = json.loads(f.read())

            name = ""

            for game in data["games"]:
                if(id == game["id"]):
                    return game["name"]

            return name

    def addAliasWithChnId(self, channel_id, alias):
        with open("databases\\game.json", "r") as f:
            data = json.loads(f.read())
            
            message = "Alias already in list"

            for game in data["games"]:
                if(game["channel_id"] == channel_id.id):
                    if(alias not in game["aliases"]):
                        game["aliases"].append(alias)
                        message =  "Alias added"

        with open("databases\\game.json", "w") as f:
            json.dump(data, f)
            return message

    def getChannelIdByGameId(self, id):
        if(id == -1):
            return -1
            print("invalid id was gived")

        with open("databases\\game.json", "r") as f:
            data = json.loads(f.read())

            r_id = -1

            for game in data["games"]:
                if id == game["id"]:
                    r_id = game["channel_id"]
        
            return r_id

    def saveToDB(self, game_id, game_name, channel_id, aliases = []):
        with open("databases\\game.json", "r") as f:
            data = json.loads(f.read())
            data["games"].append({"name":game_name,"id":game_id,"aliases":aliases,"channel_id":channel_id,"posts":[]})
        
        with open("databases\\game.json", "w") as f:
            json.dump(data, f)

    def add_post(self, game_id, post_id):
        with open("databases\\game.json", "r") as f:
            data = json.loads(f.read())
            for game in data["games"]:
                if(game["id"] == game_id):
                    game["posts"].append(post_id)
                    
        with open("databases\\game.json", "w") as f:
            json.dump(data, f)

class r_user():
    def getUserIdByName(self, name: str):
        body = {
            "usernames": [
                name
            ],
            "excludeBannedUsers": True
        }
        r = requests.post("https://users.roblox.com/v1/usernames/users", body)
        data = r.json()["data"]
        if(len(list(data)) > 0):
            return data[0]["id"]
        else:
            return 0

    def getStatus(self, userId: str):
        r = requests.get(f"https://users.roblox.com/v1/users/{userId}/status")
        data = r.json()
        if "errors" not in data:
            return data["status"]
        else:
            return data["errors"][0]["message"]

class ad():
    def __init__(self,event_description : str, discord_usr, roblox_name, game_id,timestamp,reward):
        self.event_description = event_description
        self.discord_usr = discord_usr
        self.roblox_name = roblox_name
        self.timestamp = timestamp
        self.game_id = game_id
        self.reward = reward

        self.id = str(round(timestamp)) + "-" + str(game_id)   


    def getEmbed(self):

        time_str = datetime.fromtimestamp(self.timestamp).strftime("%b %d  %I:%M %p")
        
        embed = discord.Embed(title="Play Roblox" , color=discord.Color.from_rgb(254,254,254),url="https://www.roblox.com/games/"+str(self.game_id))
        embed.add_field(name="**__GAME__**", value=games().getNameById(self.game_id),inline=False)
        embed.add_field(name="**__DESCRIPTION__**",value=self.event_description,inline=False)
        embed.add_field(name="**__TIME__**",value=time_str,inline=False)
        embed.add_field(name="**__REWARD__**",value="None; Voluntary" if self.reward == 0 else self.reward,inline=False)
        embed.add_field(name="**__ROBLOX__**",value=self.roblox_name,inline=False)
        embed.add_field(name="**__DISCORD__**", value=self.discord_usr.mention,inline=False)
        embed.set_thumbnail(url=self.discord_usr.avatar_url)
        embed.set_image(url=games().getImgUrlById(self.game_id))


        return embed

    def saveToDB(self):
        with open("databases\\posts.json", "r") as f:
            data = json.loads(f.read())
            data["posts"].append({"roblox_usr":self.roblox_name,"user_id":self.discord_usr.id,"game_id":self.game_id,"post_id":self.id,"time":self.timestamp,"reward":self.reward,"description":self.event_description})
        
        with open("databases\\posts.json", "w") as f:
            json.dump(data, f)


class posts():

    def getDictById(self, id):
        with open("databases\\posts.json", "r") as f:
            data = json.loads(f.read())

            for post in data["posts"]:
                if(id == post["id"]):
                    return post

            return {}

    def getPosts(self):
        with open("databases\\posts.json", "r") as f:
            data = json.loads(f.read())

            return data["posts"]