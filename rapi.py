import requests


class games():
    def getSorts(self):
        r = requests.get("https://games.roblox.com/v1/games/sorts")
        return r.json()

    def getList(self, sortToken: str, Max_rows: int = 20):
        r = requests.get(
            f"https://games.roblox.com/v1/games/list?model.sortToken={sortToken}&model.maxRows={Max_rows}")
        return r.json()

    def getPopular(self, Max_rows : int = 20):
        sorts = self.getSorts()["sorts"]
        token = ""
        for sort in sorts:
            if(sort["name"] == "Popular"):
                token = sort["token"]
        games_list = self.getList(token)
        return games_list

class user():
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

    def getStatus(self, userId : str):
        r = requests.get(f"https://users.roblox.com/v1/users/{userId}/status")
        data = r.json()
        if "errors" not in data:
            return data["status"]
        else:
            return data["errors"][0]["message"]