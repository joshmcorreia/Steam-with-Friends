import os
import discord
import mysql.connector
from discord.ext import commands

TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL_ID = int(os.getenv('CHANNEL_ID'))
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

@bot.event
async def on_ready():
	print("SteamWithFriendsBot is ready!")
	channel = bot.get_channel(CHANNEL_ID)
	await channel.send("SteamWithFriendsBot is ready!")

@bot.command()
async def add_user(ctx, name, steam_url):
	"""
	Adds the specified user to the database of users
	"""
	print(f"Adding user `{name}` with steam_url `{steam_url}`")
	await ctx.send(f"Adding user `{name}` with steam_url `{steam_url}`")

	# TODO: Make sure the user doesn't already exist in the database
	# TODO: Make sure the steam URL is valid

@bot.command()
async def update_games(ctx, name):
	"""
	Adds the list of games for the specified user
	"""
	pass
	# TODO: Check if the user is in the database. If they aren't, return an error

bot.run(TOKEN)
