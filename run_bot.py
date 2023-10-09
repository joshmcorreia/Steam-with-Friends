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
	"""
	server_response = steam_with_friends_bot.get_all_users()
	await ctx.send(server_response)

@bot.command()
async def update_games(ctx, player_name):
	"""
	Adds the list of games for the specified user
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

bot.run(TOKEN)
