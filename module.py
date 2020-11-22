import discord
import requests
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
                    
    def getChannelIdByGameId(self, id):
        if(id == -1):
            return -1

        with open("databases\\game.json", "r") as f:
            data = json.loads(f.read())

            id = -1

            for game in data["games"]:
                if id == game["id"]:
                    id = game["channel-id"]
        
            return id

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
    def __init__(self, discord_id, roblox_name, game_id, timestamp):
        self.discord_id = discord_id
        self.roblox_name = roblox_name
        self.timestamp = timestamp

        self.id = str(round(timestamp)) + "-" + str(game_id)   


    def getEmbed(self):
        
        embed = discord.Embed(description="Hi there", color=discord.Color.from_rgb(254,254,254))

        return embed
