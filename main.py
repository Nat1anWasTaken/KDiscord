import disnake
from disnake.ext import commands
from disnake.ui import Button
import os
import logging
from pymongo import MongoClient
from pymongo.server_api import ServerApi

# Logging
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

# Initialize the bot
intents = disnake.Intents.all()
bot = commands.Bot(command_prefix="k!", intents=intents, owner_id=int(os.getenv("OWNER_ID")))

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
    embed = disnake.Embed(title="提起告訴", description="讀完上面的訴訟說明後，點擊下方按鈕提起告訴", color=disnake.Colour.blue())
    components = [Button(label="提起告訴", emoji='🛎️', custom_id="accuse", style=disnake.ButtonStyle.primary)]
    await bot.get_channel(int(os.getenv("BELL_CHANNEL"))).send(embed=embed, components=components)


bot.run(os.getenv('TOKEN'))
