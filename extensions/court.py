import disnake
from disnake.ext import commands
from disnake.ui import Button
from disnake import ButtonStyle
from modals import Accuse


class Court(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="accuse", description="提起一個告訴", guild_ids=[921645783915319316])
    async def accuse(self, ctx):
        """
        提起一個告訴
        :param ctx: Context
        :return: None
        """
        await ctx.interaction.response.send_modal(Accuse(self.bot))

    @commands.is_owner()
    @commands.slash_command(name="send_trigger_message", description="發送觸發訊息", guild_ids=[921645783915319316])
    async def send_trigger_message(self, interaction, channel: disnake.TextChannel = None):
        """
        發送觸發訊息
        :param ctx: Context
        :param channel: The channel to send the message to
        :return:
        """
        if channel is None:
            channel = interaction.channel
        embed = disnake.Embed(title="提起告訴", description="讀完上面的訴訟說明後，點擊下方按鈕提起告訴", color=disnake.Colour.blue())
        components = [Button(label="提起告訴", emoji='🛎️', custom_id="accuse", style=disnake.ButtonStyle.primary)]
        await channel.send(embed=embed, components=components)
        await interaction.response.send_message("Message Sent!", ephemeral=True)


def setup(bot):
    bot.add_cog(Court(bot))
