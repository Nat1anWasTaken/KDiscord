import discord
import errors
import utils
from discord.ui import Modal, InputText, View
from discord import InputTextStyle
import asyncio
from buttons.accept import Accept
import os


class Accuse(Modal):
    def __init__(self, bot):
        """
        A Accuse modal.
        :param bot Your bot instance, used to get the channel.
        """
        super().__init__("提起告訴")
        self.add_item(InputText(label="被告人", placeholder="凱恩Kane#5384 (多使用者以,分隔)", required=True))
        self.add_item(InputText(label="希望的受理人", placeholder="任意一位小幫手或是管理員", required=False))
        self.add_item(InputText(label="原因", placeholder="他太佬了!", required=True, style=InputTextStyle.long))
        self.bot = bot

    async def callback(self, interaction):
        embed = discord.Embed(title="新的案件", color=discord.Colour.yellow())

        # Find defendants
        defendants = await utils.find_user_by_name_and_tag(self.children[0].value, interaction.guild,
                                                           multiple=True)
        embed.add_field(name="被告人", value=", ".join([str(x) for x in defendants]))

        # Find assignee
        try:
            assignee = await utils.find_user_by_name_and_tag(self.children[1].value, interaction.guild, multiple=False)
            content = assignee.mention
        except errors.UnparseableText:
            assignee = None
            content = None

        # Prepare the embed
        embed.add_field(name="預期受理人", value=content)
        embed.add_field(name="原因", value=self.children[2].value)
        # Admin Side
        case_message = await self.bot.get_channel(int(os.getenv("CASES_CHANNEL"))).send(content=content,
                                                                                             embed=embed)
        embed.set_footer(text="案件編號: " + str(case_message.id))
        view = View()
        view.add_item(Accept(bot=self.bot, case_id=case_message.id))
        await case_message.edit(content=content, embed=embed, view=view)
        # User Side
        replied_interaction = await interaction.response.send_message(
            content=f"{interaction.user.mention} 你的案件已送出並等待審理!", embed=embed)
        asyncio.get_event_loop().create_task(replied_interaction.delete_original_message(delay=10))
