import requests
import xmltodict

class User:
    def __init__(self, username, url):
        self.username = username
        self.url = url
        self.games_dict = set()
        self.download_game_list()

    def download_game_list(self):
        print(f"Loading {self.username}'s games...")
        try:
            games_url = self.url + "/games?tab=all&xml=1"
            response = requests.get(games_url).content.decode()
            parsed_dict = xmltodict.parse(response)
            for game in parsed_dict["gamesList"]["games"]["game"]:
                game_name = game["name"]
                self.games_dict.add(game_name)
        except KeyError:
            print(f"ERROR: The user {self.username} seems to have their profile set to private")
