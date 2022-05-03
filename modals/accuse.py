import disnake
import errors
import utils
from utils import ErrorEmbed
from disnake.ui import Modal, View, Button, TextInput
from disnake import TextInputStyle
import os


class Accuse(Modal):
    def __init__(self, bot):
        """
        A Accuse modal.
        :param bot Your bot instance, used to get the channel.
        """
        components = []
        components.append(TextInput(label="被告人",
                                    placeholder="凱恩Kane#5384 (多使用者以,分隔)",
                                    required=True,
                                    style=TextInputStyle.short,
                                    custom_id="defendants"))
        components.append(TextInput(label="希望的受理人",
                                    placeholder="任意一位小幫手或是管理員",
                                    required=False,
                                    style=TextInputStyle.short,
                                    custom_id="assignee"))
        components.append(TextInput(label="原因",
                                    placeholder="他太佬了!",
                                    required=True,
                                    style=TextInputStyle.paragraph,
                                    custom_id="reason"))
        super().__init__(title="提起告訴", custom_id="accuse", components=components)
        self.bot = bot

    async def callback(self, interaction):
        embed = disnake.Embed(title="新的案件", color=disnake.Colour.yellow())

        # Find defendants
        defendants = await utils.find_user_by_name_and_tag(interaction.text_values["defendants"],
                                                           interaction.guild,
                                                           multiple=True)
        if len(defendants) <= 0:
            await interaction.response.send_message(embed=ErrorEmbed("被告人不存在"), ephemeral=True)
            return
        embed.add_field(name="被告人", value=", ".join([x.mention for x in defendants]))

        # Find assignee
        if not interaction.text_values["assignee"] == "":
            try:
                assignee = await utils.find_user_by_name_and_tag(interaction.text_values["assignee"], interaction.guild,
                                                                 multiple=False)
                embed.add_field(name="預期受理人", value=assignee.mention)
            except errors.UnparseableText:
                await interaction.response.send_message(embed=ErrorEmbed("受理人不存在"), ephemeral=True)
                return
        else:
            assignee = None
            content = None


        # Prepare the embed
        embed.add_field(name="原因", value=interaction.text_values["reason"])
        # Admin Side
        case_message = await self.bot.get_channel(int(os.getenv("CASES_CHANNEL"))).send(content=content,
                                                                                        embed=embed)
        embed.set_footer(text="案件編號: " + str(case_message.id))
        view = View()
        view.add_item(
            Button(label="審理", emoji="✅", style=disnake.ButtonStyle.primary, custom_id=f"accept.{case_message.id}"))
        await case_message.edit(content=content, embed=embed, view=view)
        # User Side
        replied_interaction = await interaction.response.send_message(
            content=f"{interaction.user.mention} 你的案件已送出並等待審理!", embed=embed, ephemeral=True)

        del replied_interaction, view, embed, content

        # Register the case to database
        data = {
            "complainant": interaction.user.id,
            "defendants": [x.id for x in defendants],
            "assignee": assignee.id if assignee else None,
            "reason": interaction.text_values["reason"],
            "id": case_message.id,
            "status": {
                "accepted": "pending",
                "assignee": None,
            }
        }
        self.bot.db.cases.insert_one(data)
