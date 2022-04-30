import discord
from discord.ext import commands
import os
import logging
import json

# Initialize the bot
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="k!", intents=intents)

# Load config file
with open('config.json') as config_file:
    config = json.load(config_file)
    bot.config = config
    bot.owner_id = config['owner']

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)


@bot.event
async def on_ready():
    logging.info(f"Bot is ready! Logged in as {bot.user}")
    for file in os.listdir("./extensions"):
        if file.endswith(".py"):
            bot.load_extension(f"extensions.{file[:-3]}")
            logging.info(f"Loaded extension {file[:-3]}")
    logging.info("Done loading extensions")


bot.run(os.getenv('TOKEN'))
