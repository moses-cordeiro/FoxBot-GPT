import discord, json, logging
from discord.ext import commands
from discord.commands import SlashCommandGroup
from helpers import db_manager

class Setup(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  async def is_admin(ctx):
    return ctx.author.guild_permissions.administrator
  
  def initialized(self, guild_id):
    if db_manager.get_guild_id((guild_id,)) is not None:
      return True
    return False
  
  setup = SlashCommandGroup("setup","setup")

  @setup.command()
  @commands.check(is_admin)
  async def init(self, ctx):
    if self.initialized(ctx.guild.id):
      await ctx.respond("You have already initialized FoxBot for this server!", ephemeral=True)
    else:
      guild_id = ctx.guild.id
      db_manager.initialize_server((guild_id, None, None))
      await ctx.response.send_message("Server initialized!")
      self.initialized = True

  @init.error
  async def setup_error(self, ctx, error):
    if isinstance(error, discord.errors.CheckFailure):
      await ctx.respond("You do not have permission to run this command.", ephemeral=True)
    else:
      raise error

def setup(bot):
  bot.add_cog(Setup(bot))
  print(f"Setup cog loaded - {__name__}")

def teardown(bot):
  bot.remove_cog(Setup(bot))
  print("Setup cog unloaded")
    