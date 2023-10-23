import os
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Load config files
with open('config/foxbot.json') as f:
  foxbot_config = json.load(f)

with open('config/chat.json') as f:
  chat_config = json.load(f)

with open('config/logging.json') as f:
  logging_config = json.load(f)

# Access environment variables
class Mars(enumerate):
  URL:str = chat_config.mars.url
  TOKEN:str = os.getenv('MARS_TOKEN')

class OpenAI(enumerate):
  URL:str = chat_config.openai.url
  TOKEN:str = os.getenv('OPENAI_TOKEN')

class Discord(enumerate):
  URL:str = foxbot_config.discord.url
  TOKEN:str = os.getenv('DISCORD_TOKEN')

class Log(enumerate):
  CONFIG:dict = logging_config