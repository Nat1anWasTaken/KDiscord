import discord
import utils
from discord.ui import Modal, InputText
from discord import InputTextStyle
import asyncio


class Accuse(Modal):
    def __init__(self, bot) -> None:
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
        embed = discord.Embed(title="新的案件", color=discord.Colour.yellow())  # Initialization the embed

        # Find defendants
        print(self.children[0].value)
        print(type(self.children[0].value))
        defendants = await utils.find_user_by_name_and_tag(self.children[0].value, interaction.guild,
                                                           multiple=True)
        embed.add_field(name="被告人", value=", ".join([str(x) for x in defendants]))

        # Find assignee
        assignee = await utils.find_user_by_name_and_tag(self.children[1].value, interaction.guild)
        embed.add_field(name="預期受理人", value=assignee)
        embed.add_field(name="原因", value=self.children[2].value)  # Add the reason to the embed
        await self.bot.get_channel(self.bot.config["channels"]["cases"]).send(embed=embed)  # Send the embed
        await interaction.response.pong()
        message = await interaction.channel.send(content=f"{interaction.user.mention} 你的案件已送出並等待審理!", embed=embed)
        await asyncio.sleep(10)
        await message.delete()
