import re
import requests
import xmltodict
from BetterLogger import logger

class InvalidSteamURLException(Exception):
	pass

class PrivateProfileException(Exception):
	pass

class PrivateGameListException(Exception):
	pass

class SteamUser:
	def __init__(self, steam_url: str):
		self.steam_url = steam_url
		self.games_set = set()
		self.validate_steam_url()
		self.get_game_list()

	def validate_steam_url(self):
		"""
		Validates the Steam URL to see if it matches a basic regex
		"""
		match = re.search("^https:\/\/steamcommunity.com\/", self.steam_url)
		if match is None:
			raise InvalidSteamURLException(f"Invalid SteamURL `{self.steam_url}`")

	def get_game_list(self):
		try:
			games_url = self.steam_url + "/games?tab=all&xml=1"
			response = requests.get(games_url).content.decode()
			parsed_dict = xmltodict.parse(response)
			for game in parsed_dict["gamesList"]["games"]["game"]:
				game_name = game["name"]
				self.games_set.add(game_name)
		except KeyError as err:
			logger.error(f"KeyError: {err}")
			logger.exception(err)
			error_message = f"ERROR: The user {self.steam_url} seems to have their profile set to private!"
			raise PrivateProfileException(error_message)
		except TypeError as err:
			logger.error(f"TypeError: {err}")
			logger.exception(err)
			error_message = f"ERROR: The user {self.steam_url} seems to have the games list on their profile set to private!"
			raise PrivateGameListException(error_message)
