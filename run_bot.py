import os
import discord
from discord.ext import commands
from SteamWithFriendsBot import SteamWithFriendsBot
from SteamUser import PrivateProfileException, PrivateGameListException

TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL_ID = int(os.getenv('CHANNEL_ID'))
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
steam_with_friends_bot = SteamWithFriendsBot()

@bot.event
async def on_ready():
	print("SteamWithFriendsBot is ready!")
	channel = bot.get_channel(CHANNEL_ID)
	await channel.send("SteamWithFriendsBot is ready!")

@bot.command()
async def add_user(ctx, name, steam_url):
	"""
	Adds the specified user to the database of users

	Example:
	!add_user Josh https://steamcommunity.com/id/Winning117/
	"""
	try:
		steam_with_friends_bot.add_user(steam_url=steam_url, name=name)
		await ctx.send(f"Added user `{name}` with steam_url `{steam_url}`")
	except PrivateProfileException:
		await ctx.send(f"Failed to add user `{name}` because their Steam profile is set to private.")
	except PrivateGameListException:
		await ctx.send(f"Failed to add user `{name}` because their games list is set to private.")
	except Exception as err:
		await ctx.send(f"Failed to add user `{name}` due to an unexpected exception.")

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
	try:
		steam_with_friends_bot.update_user_games(player_name=player_name)
		await ctx.send(f"Successfully updated games for {player_name}")
	except Exception as err:
		await ctx.send(f"Failed to update {player_name}'s games due to an unexpected error. Reason: {err}")

bot.run(TOKEN)
