# Pip Modules
import discord, os, time
from discord.ext import commands
from dotenv import dotenv_values
import sqlite3

# Local Modules
from config import Discord

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(allowed_mentions=discord.AllowedMentions(roles=True, users=True, everyone=False), intents=intents)

@bot.event
async def on_message(message):
  if not message.author.bot:
    await bot.process_commands(message)

@bot.slash_command(description = "Load a cog")
@commands.is_owner()
async def load(ctx, extension):
  bot.load_extension(f'cogs.{extension}')
  await ctx.send(f'Loaded {extension} cog')

@bot.slash_command(description = "Unload a cog")
@commands.is_owner()
async def unload(ctx, extension):
  bot.unload_extension(f'cogs.{extension}')
  await ctx.send(f'Unloaded {extension} cog')

@bot.slash_command(description = "Reload a cog")
@commands.is_owner()
async def reload(ctx, extension):
  bot.reload_extension(f'cogs.{extension}')
  await ctx.send(f'Reloaded {extension} cog')

# TODO -> This should probably be in db_manager.py
@bot.event
async def on_ready():
  db = sqlite3.connect('database.db')
  cursor = db.cursor()

  # User Likability is the likability of a given user, regardless of server.
  # It determines the likability of the user in any server, and how often foxbot will interact with them
  # Likability index is calculated by taking the totial interactions, and how often negative interactions occur
  # 90 likability is basically romance, and 0 is basically hatred

  # player_id - the discord id of the user
  # positive_interactions - the number of positive interactions foxbot has had with the user
  # negative_interactions - the number of negative interactions foxbot has had with the user
  # likability_index - (total_interactions - negative_interactions) / total_interactions * 100
  # last_interaction_time - the time of the last interaction with the user
  cursor.execute(
    '''
    CREATE TABLE IF NOT EXISTS player_likability(
    player_id INTEGER PRIMARY KEY,
    positive_interactions INTEGER,
    negative_interactions INTEGER,
    likability_index INTEGER,
    last_interaction_time INTEGER
    )
    '''
  )

  # Server Likability is the likability of the server as a whole
  # It determines how often foxbot will check that server, and participate in conversations
  # Additionally, it lightly influences the likability of users in that server
  # Likability index is calculated daily by taking the total interactions, and how often negative interactions occur,
  # in addition to the amount of average likability foxbot has of players in that given server.
  cursor.execute(
    '''
    CREATE TABLE IF NOT EXISTS server_likability(
    player_id INTEGER PRIMARY KEY,
    positive_interactions INTEGER,
    negative_interactions INTEGER,
    likability_index INTEGER,
    last_interaction_time INTEGER
    )
    '''
  )
  db.commit()

if __name__ == "__main__":
  # Setup Logging
  import logging.config
  logging.config.dictConfig('config/logging.json')


  # load cogs
  for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
      bot.load_extension(f'cogs.{filename[:-3]}')
  
  bot.run(Discord.TOKEN)