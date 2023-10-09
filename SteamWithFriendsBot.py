import mysql.connector
from SteamUser import SteamUser

class PlayerNameDoesNotExistException(Exception):
	pass

class SteamWithFriendsBot:
	def __init__(self) -> None:
		self.database_username = "root"
		self.database_password = "password"
		self.database_ip = "192.168.1.68"
		self.database_name = "steam_with_friends_bot"
		self.connect_to_database()

	def connect_to_database(self):
		self.database_connection = mysql.connector.connect(user=self.database_username, password=self.database_password, host=self.database_ip, database=self.database_name)
		self.database_cursor = self.database_connection.cursor()

	def get_all_users(self):
		select_sql_statement = "SELECT * FROM `Users`"
		self.database_cursor.execute(select_sql_statement)
		database_response = self.database_cursor.fetchall()
		return database_response

	def add_user_to_database(self, steam_url, player_name):
		"""
		Adds a user's SteamID and PlayerName to the database

		Fails if the user already exists
		"""
		insert_sql_statement = "INSERT INTO `Users` (`SteamPlayerID`, `PlayerName`) VALUES (%s, %s)"
		sql_arguments = (steam_url, player_name,) # a tuple is expected so we need the trailing comma
		self.database_cursor.execute(insert_sql_statement, sql_arguments)
		self.database_connection.commit()

	def convert_player_name_to_steam_id(self, player_name):
		select_sql_statement = "SELECT * FROM Users WHERE PlayerName=%s"
		sql_arguments = (player_name,) # a tuple is expected so we need the trailing comma
		self.database_cursor.execute(select_sql_statement, sql_arguments)
		database_response = self.database_cursor.fetchall()
		if len(database_response) == 0:
			raise PlayerNameDoesNotExistException(f"The player `{player_name}` does not exist in the database.")
		return database_response[0][0] # [0] for the first row, and [0] to get the SteamPlayerID from the list

	def add_game_to_database(self, game_name, player_name):
		insert_sql_statement = "INSERT IGNORE INTO `Games` (`GameName`, `PlayerName`) VALUES (%s, %s)"
		sql_arguments = (game_name, player_name,) # a tuple is expected so we need the trailing comma
		self.database_cursor.execute(insert_sql_statement, sql_arguments)
		self.database_connection.commit()

	def add_user(self, steam_url, player_name):
		steam_user = SteamUser(steam_url=steam_url) # calling this will throw exceptions if the user cannot be loaded correctly
		self.add_user_to_database(steam_url=steam_url, player_name=player_name)
		for game in steam_user.games_set:
			self.add_game_to_database(game_name=game, player_name=player_name)

	def update_user_games(self, player_name):
		steam_player_id = self.convert_player_name_to_steam_id(player_name=player_name)
		steam_user = SteamUser(steam_url=steam_player_id)
		for game in steam_user.games_set:
			self.add_game_to_database(game_name=game, player_name=player_name)

	def get_games_in_common(self, users: tuple):
		select_sql_statement = "select GameName from Games WHERE "
		for user in users:
			select_sql_statement += "PlayerName=%s OR "
		select_sql_statement = select_sql_statement[:-3] # remove the last "OR "
		select_sql_statement += f"GROUP BY GameName HAVING COUNT(*) = {len(users)};"
		sql_arguments = users # a tuple is expected so we need the trailing comma
		print(select_sql_statement)
		print(sql_arguments)
		self.database_cursor.execute(select_sql_statement, sql_arguments)
		database_response = self.database_cursor.fetchall()
		return database_response
