from .errors import NotOwner
from disnake import Interaction


class SlashCommandCheck:
    def __init__(self):
        pass

    @staticmethod
    def is_owner(interaction: Interaction):
        if interaction.author.id != interaction.bot.owner_id:
            raise NotOwner
