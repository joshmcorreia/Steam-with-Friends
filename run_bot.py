import os
import discord
import mysql
from discord.ext import commands
from SteamWithFriendsBot import SteamWithFriendsBot, PlayerNameDoesNotExistException
from SteamUser import InvalidSteamURLException, PrivateProfileException, PrivateGameListException
from BetterLogger import logger

TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL_ID = int(os.getenv('CHANNEL_ID'))
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
steam_with_friends_bot = SteamWithFriendsBot()

@bot.command()
async def add_user(ctx, player_name, steam_url):
	"""
	Adds the specified user to the database of users

	Example:
	!add_user Josh https://steamcommunity.com/id/Winning117/
	"""
	player_name_lowercase = player_name.lower() # always force the player_name to be lowercase so the user can use any variation of capitalization
	try:
		steam_with_friends_bot.add_user(steam_url=steam_url, player_name=player_name_lowercase)
		await ctx.send(f"Added user `{player_name}` with steam_url `{steam_url}`")
	except PrivateProfileException:
		await ctx.send(f"Failed to add user `{player_name}` because their Steam profile is set to private.")
	except PrivateGameListException:
		await ctx.send(f"Failed to add user `{player_name}` because their games list is set to private.")
	except InvalidSteamURLException:
		await ctx.send(f"Failed to add user `{player_name}` because the URL `{steam_url}` is invalid. The URL should match the form `https://steamcommunity.com/id/STEAM_ID`.")
	except mysql.connector.errors.IntegrityError as err:
		await ctx.send(f"Failed to add user `{player_name}` because they are already in the database.")
	except Exception as err:
		logger.exception(err)
		await ctx.send(f"Failed to add user `{player_name}` due to an unexpected exception.")

	# TODO: Make sure the user doesn't already exist in the database
	# TODO: Make sure the steam URL is valid

@bot.command()
async def get_users(ctx):
	"""
	Returns a list of all users currently in the database

	Example:
	!get_users
	"""
	server_response = steam_with_friends_bot.get_all_users()
	users_string = ""
	for user in server_response:
		steam_player_id = user[0]
		player_name = user[1]
		users_string += f"{player_name} - `{steam_player_id}`\n"
	await ctx.send(users_string)

@bot.command()
async def update_games(ctx, player_name):
	"""
	Adds the list of games for the specified user

	Example:
	!update_games Josh
	"""
	player_name_lowercase = player_name.lower() # always force the player_name to be lowercase so the user can use any variation of capitalization
	try:
		steam_with_friends_bot.update_user_games(player_name=player_name_lowercase)
		await ctx.send(f"Successfully updated games for {player_name}")
	except PlayerNameDoesNotExistException as err:
		error_message = f"Unrecognized user `{player_name}`. Add them as a new user first!"
		logger.error(error_message)
		logger.exception(err)
		await ctx.send(error_message)
	except Exception as err:
		error_message = f"Failed to update {player_name}'s games due to an unexpected exception."
		logger.error(error_message)
		logger.exception(err)
		await ctx.send(error_message)

@bot.command()
async def play(ctx, *users):
	"""
	Returns a list of games that all players own

	Example:
	!play Josh Stell Colin
	"""
	if len(users) < 2:
		error_message = "The !play command requires two or more players."
		logger.error(error_message)
		await ctx.send(error_message)

	games_in_common = steam_with_friends_bot.get_games_in_common(users=users)
	games_in_common_as_string = ""
	for game in games_in_common:
		games_in_common_as_string += f"{game[0]}\n"
	print(games_in_common)
	await ctx.send(games_in_common_as_string[:1999])
	# TODO: deal with sending messages >2000 characters
	# TODO: add option for users to randomly get a game from the list

bot.run(TOKEN)
