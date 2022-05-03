import disnake
import utils
from utils import errors
from utils.embeds import *
from disnake.ui import Modal, View, Button, TextInput
from disnake import TextInputStyle
import os
import time


class Accuse(Modal):
    def __init__(self, bot):
        """
        A Accuse modal.
        :param bot Your bot instance, used to get the channel.
        """
        components = [TextInput(label="被告人",
                                placeholder="凱恩Kane#5384 (多使用者以,分隔)",
                                required=True,
                                style=TextInputStyle.short,
                                custom_id="defendants"),
                      TextInput(label="希望的受理人",
                                placeholder="任意一位小幫手或是管理員",
                                required=False,
                                style=TextInputStyle.short,
                                custom_id="assignee"),
                      TextInput(label="原因",
                                placeholder="他太佬了!",
                                required=True,
                                style=TextInputStyle.paragraph,
                                custom_id="reason")]
        super().__init__(title="提起告訴", custom_id="accuse", components=components)
        self.bot = bot

    async def callback(self, interaction):
        # Check if the user already have a pending accusation
        data = self.bot.db.cases.find_one({"complainant": interaction.author.id})
        if data is not None:
            await interaction.response.send_message(embed=ErrorEmbed("一個人最高只能有一個處理中的案件！"), ephemeral=True)
            return
        # Find defendants
        defendants = await utils.find_user_by_name_and_tag(interaction.text_values["defendants"],
                                                           interaction.guild,
                                                           multiple=True)
        if len(defendants) <= 0:
            await interaction.response.send_message(embed=ErrorEmbed("被告人不存在"), ephemeral=True)
            return

        # Find assignee
        if not interaction.text_values["assignee"] == "":
            try:
                assignee = await utils.find_user_by_name_and_tag(interaction.text_values["assignee"], interaction.guild,
                                                                 multiple=False)
            except errors.UnparseableText:
                await interaction.response.send_message(embed=ErrorEmbed("受理人不存在"), ephemeral=True)
                return
        else:
            assignee = None
            content = None

        # Generate case ID
        case_message = await self.bot.get_channel(int(os.getenv("CASES_CHANNEL"))).send("Generating case ID...")

        # Register the case to database
        data = {
            "complainant": interaction.user.id,
            "defendants": [x.id for x in defendants],
            "assignee": assignee.id if assignee else None,
            "reason": interaction.text_values["reason"],
            "id": case_message.id,
            "status": {
                "status": "pending",
                "assignee": None,
                "appeal": False
            }
        }

        embed = CaseEmbed(bot=self.bot, data=data)

        view = View()
        view.add_item(Button(label="審理", emoji="✅", style=disnake.ButtonStyle.primary, custom_id=f"accept.{case_message.id}"))
        view.add_item(Button(label="拒絕", emoji="❌", style=disnake.ButtonStyle.danger, custom_id=f"reject.{case_message.id}"))
        await case_message.edit(content=content, embed=embed, view=view)
        # User Side
        await interaction.response.send_message(
            content=f"{interaction.user.mention} 你的案件已送出並等待審理!", embed=embed, ephemeral=True)
        await interaction.user.send(content=f"提告紀錄 <t:{round(time.time())}:F>", embed=embed)
        self.bot.db.cases.insert_one(data)
