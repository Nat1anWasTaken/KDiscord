import discord
from discord.ui import Button


class Accept(Button):
    def __init__(self, bot, case_id):
        """
        A button for admin to accept a case.
        """
        super().__init__(label="審理", emoji="✅", style=discord.ButtonStyle.primary, custom_id=f"accept.{case_id}")
        self.bot = bot

    async def callback(self, interaction):
        pass
