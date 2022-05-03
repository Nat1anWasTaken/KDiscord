import asyncio

import disnake
from disnake.ext import commands
from utils import has_admin, ErrorEmbed
from modals import Accuse
from modals import ConfirmCase


class Buttons(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener(name="on_interaction")
    async def on_interaction(self, interaction):
        if interaction.type == disnake.InteractionType.component:
            if interaction.data.custom_id.startswith("accept."):
                asyncio.get_event_loop().create_task(self.accept(interaction))
            elif interaction.data.custom_id == "accuse":
                await interaction.response.send_modal(Accuse(self.bot))

    async def accept(self, interaction):
        if not await has_admin(member=interaction.user):
            await interaction.response.send_message(embed=ErrorEmbed(f"{interaction.user.mention} 你沒有權限使用這個按鈕"),
                                                    delete_after=3)
            return

        case_id = int(interaction.data.custom_id.split(".")[1])
        # Check is the case in database
        case = self.bot.db.cases.find_one({"id": case_id})
        if case is None:
            await interaction.response.send_message(embed=ErrorEmbed(f"{interaction.user.mention} 找不到這個案件"),
                                                    delete_after=3)
            return
        await interaction.response.send_modal(ConfirmCase(self.bot))


def setup(bot):
    bot.add_cog(Buttons(bot))
