import discord
from discord.ext import commands
import os
import logging
from pymongo import MongoClient
from pymongo.server_api import ServerApi

# Logging
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

# Initialize the bot
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="k!", intents=intents)

# Connect to mongodb
mongo = MongoClient(os.getenv("MONGO_DB_URL"), server_api=ServerApi('1'))
bot.db = mongo.main


@bot.event
async def on_ready():
    logging.info(f"Bot is ready! Logged in as {bot.user}")
    for file in os.listdir("./extensions"):
        if file.endswith(".py"):
            bot.load_extension(f"extensions.{file[:-3]}")
            logging.info(f"Loaded extension {file[:-3]}")
    logging.info("Done loading extensions")


bot.run(os.getenv('TOKEN'))
