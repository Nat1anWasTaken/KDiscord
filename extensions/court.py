import discord
from discord.ext import commands
from discord.ui import View
from modals.accuse import Accuse
from buttons.bell import Bell


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
    async def send_trigger_message(self, ctx, channel: discord.TextChannel):
        """
        發送觸發訊息
        :param ctx: Context
        :param channel: The channel to send the message to
        :return:
        """
        embed = discord.Embed(title="鈴鐺", description="讀完上面的訴訟說明後，點擊下方按鈕提起告訴", color=discord.Colour.blue())
        view = View()
        view.add_item(Bell(self.bot))
        await channel.send(embed=embed, view=view)


def setup(bot):
    bot.add_cog(Court(bot))
