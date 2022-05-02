import discord
from discord.ui import Modal, InputText, View


class ConfirmCase(Modal):
    def __init__(self, bot, assignee=False):
        """
        A modal to confirm the case.
        :param bot: Bot instance
        :param assignee: Is the user that accepted the case the wanted-assignee?
        """
        if not assignee:
            super().__init__("你不是這個案件的預期受理人，確定要審理這個案件嗎?")
            self.add_item(InputText(label="輸入`yes`來確認", required=True))
            self.bot = bot
        else:
            super().__init__("確定審理案件?")
            self.add_item(InputText(label="輸入`yes`來確認", required=True))
            self.bot = bot

    async def callback(self, interaction):
        if self.children[0].value == "YES":
            case_message = interaction.message
            self.bot.db.cases.update_one({"id": case_message.id}, {"$set": {"status": {"accepted": True, "assignee": interaction.user.id}}})
            # Add assignee to the case and change the status to accepted
            new_embed = case_message.embeds[0]
            new_embed.add_field(name="受理人", value=interaction.user.mention)
            new_embed.colour = discord.Colour.green()
            # Remove buttons
            new_view = View()
            await interaction.response.edit_message(embed=new_embed, view=new_view)

