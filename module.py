import discord
from discord.utils import get
import requests
from datetime import * 
import json
from src import guild_info

class user():
    def __init__(self, id : str):
        self.id = id
    
    def addInfraction(self):
        data = db("users").getDb()
        if(data["users"]):
            for user in data["users"]:
                if user["id"] == self.id:
                    try:
                        user["infractions"] += 1
                    except:
                        return False
            db("users").saveDb(data)
            return True
        else:
            return False

    def setInfractions(self,n):
        data = db("users").getDb()
        if(data["users"]):
            for user in data["users"]:
                if user["id"] == self.id:
                    try:
                        user["infractions"] = n
                    except:
                        return False
            db("users").saveDb(data)
            return True
        else:
            return False

    def setDescription(self, description : str):
        data = db("users").getDb()
        if(data["users"]):
            for user in data["users"]:
                if user["id"] == self.id:
                    try:
                        user["description"] = description
                    except:
                        return False
            db("users").saveDb(data)
            return True
        else:
            return False

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
    def __init__(self,event_description : str, discord_usr : discord.User, roblox_name, game_id,timestamp,reward):
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
        embed.add_field(name="\u200b\n",value=self.event_description,inline=False)
        embed.add_field(name="**__TIME__**",value=time_str,inline=False)
        embed.add_field(name="**__REWARD__**",value="None; Voluntary" if self.reward == 0 else self.reward,inline=False)
        embed.add_field(name="**__CONTACT__**", value='[:roblox:{}](https://web.roblox.com/users/{})\n:discord:{}'.format(self.roblox_name,r_user().getUserIdByName(self.roblox_name),self.discord_usr.mention),inline=False)
        embed.set_thumbnail(url=self.discord_usr.avatar_url)
        embed.set_image(url=games().getImgUrlById(self.game_id))

        return embed

    def saveToDB(self):
        with open("databases\\posts.json", "r") as f:
            data = json.loads(f.read())
            data["posts"].append({"roblox_usr":self.roblox_name,"user_id":self.discord_usr.id,"game_id":self.game_id,"post_id":self.id,"time":self.timestamp,"reward":self.reward,"description":self.event_description})
        
        with open("databases\\posts.json", "w") as f:
            json.dump(data, f)

class db():
    def __init__(self,db : str):
        self.db = db
    
    def saveDb(self,data):
        try:
            with open(f"databases\\{self.db}.json", "w") as f:
                try:
                    f.write(json.dumps(data))
                except TypeError:
                    return False
                return True
        except FileNotFoundError:
            return False

    def getDb(self):
        try:
            with open(f"databases\\{self.db}.json", "r") as f:
                try:
                    return json.loads(f.read())
                except TypeError:
                    return False
        except FileNotFoundError:
            return False
            
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

class ticket():
    def __init__(self, user, reason):
        self.reason = reason
        self.user = user
        self.id = 0

        data = db("tickets").getDb()["tickets"]
        max_id = 0
        for ticket in data:
            max_id = max(max_id, ticket["id"])
            if ticket["poster"] == self.user and ticket["reason"] == self.reason:
                self.id = ticket["id"]
                break
        self.id = max_id+1

    def get_json(self):
        return {"id":self.id, "poster":str(self.user.id), "reason":self.reason}

    def save(self):
        data = db("tickets").getDb()
        for t in data["tickets"]:
            if t["poster"] == str(self.user.id) and t["reason"] == self.reason:
                return
        data["tickets"].append(self.get_json())
        db("tickets").saveDb(data)

    def get_embed(self, ctx):
        embed = discord.Embed(description="**Reason for support ticket**" + "\n" + self.reason + "\n\n" + guild_info.support_footer.replace("[support]", get(ctx.guild.roles, id=int(guild_info.support)).mention))
        embed.add_field(name="**id**",value=str(self.id))
        return embed
        
    def get_cat(self, ctx):
        cat = get(ctx.guild.categories, id=int(guild_info.support_category))
        if cat == None:
            cat = ctx.guild.categories[0]
        return cat

    async def get_channel(self,ctx):
        cat = self.get_cat(ctx)
        channel_name = f"ticket {self.id}"
        channel = get(ctx.guild.text_channels, name=channel_name)
        if channel != None:
            return channel
        

        channel = await cat.create_text_channel(channel_name, reason="Channel for a support case")
        
        overwrite = discord.PermissionOverwrite()
        overwrite.send_messages = False
        overwrite.read_messages = False

        await channel.set_permissions(get(ctx.guild.roles,name="@everyone"), overwrite=overwrite)
        
        perms = channel.overwrites_for(self.user)
        perms.send_messages = True
        perms.read_messages = True

        await channel.set_permissions(self.user, overwrite=perms)
        
        return channel

async def getTicketIdByChannelId(guild,channel_id):
    
    channel = get(guild.channels, id=channel_id)
    
    pins = await channel.pins()
    id_pin = pins[len(pins)-1]
    id_msg = id_pin.embeds[0].to_dict()
    id = int(id_msg["fields"][0]["value"])
    
    return id