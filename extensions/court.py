import discord
import asyncio
from utils import has_admin
from discord.ext import commands
from discord.ui import View
from modals.accuse import Accuse
from buttons.bell import Bell
from modals.confirm_case import ConfirmCase
from utils import ErrorEmbed


class Court(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="accuse", description="提起一個告訴")
    async def accuse(self, ctx):
        """
        提起一個告訴
        :param ctx: Context
        :return: None
        """
        await ctx.interaction.response.send_modal(Accuse(self.bot))

    @commands.is_owner()
    @commands.command(name="send_trigger_message", description="發送觸發訊息")
    async def send_trigger_message(self, ctx, channel: discord.TextChannel = None):
        """
        發送觸發訊息
        :param ctx: Context
        :param channel: The channel to send the message to
        :return:
        """
        if channel is None:
            channel = ctx.channel
        embed = discord.Embed(title="鈴鐺", description="讀完上面的訴訟說明後，點擊下方按鈕提起告訴", color=discord.Colour.blue())
        view = View()
        view.add_item(Bell(self.bot))
        await channel.send(embed=embed, view=view)

    @commands.Cog.listener(name="on_interaction")
    async def on_interaction(self, interaction):
        if interaction.type == discord.InteractionType.component:
            if interaction.custom_id.startswith("accept."):  # Check if the interaction is an accept button
                if not await has_admin(member=interaction.user):
                    await interaction.response.send_message(embed=ErrorEmbed(f"{interaction.user.mention} 你沒有權限使用這個按鈕"), delete_after=3)
                    return

                case_id = int(interaction.custom_id.split(".")[1])
                # Check is the case in database
                case = self.bot.db.cases.find_one({"id": case_id})
                if case is None:
                    await interaction.response.send_message(embed=ErrorEmbed(f"{interaction.user.mention} 找不到這個案件"), delete_after=3)
                    return
                await interaction.response.send_modal(ConfirmCase(self.bot))


def setup(bot):
    bot.add_cog(Court(bot))
