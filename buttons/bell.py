import discord
from discord.ui import Button
from modals.accuse import Accuse


class Bell(Button):
    def __init__(self, bot):
        """
        A bell button that starts a accuse
        """
        super().__init__(label="敲玲", emoji="🔔", style=discord.ButtonStyle.primary)
        self.bot = bot

    async def callback(self, interaction):
        await interaction.response.send_modal(Accuse(self.bot))

