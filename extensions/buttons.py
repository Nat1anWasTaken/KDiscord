import asyncio

import disnake
from disnake.ext import commands
from disnake.ui import Button

from utils import has_admin
from utils.embeds import ErrorEmbed, SuccessEmbed
from utils.modals import Accuse


class Buttons(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener(name="on_interaction")
    async def on_interaction(self, interaction):
        if interaction.type == disnake.InteractionType.component:
            if interaction.data.custom_id.startswith("accept."):
                asyncio.get_event_loop().create_task(self.accept(interaction))
            elif interaction.data.custom_id.startswith("reject"):
                asyncio.get_event_loop().create_task(self.reject(interaction))
            elif interaction.data.custom_id == "accuse":
                await interaction.response.send_modal(Accuse(self.bot))

    async def accept(self, interaction):
        if not await has_admin(member=interaction.user):
            await interaction.response.send_message(embed=ErrorEmbed(f"{interaction.user.mention} 你沒有權限使用這個按鈕"),
                                                    ephemeral=True)
            return

        case_id = int(interaction.data.custom_id.split(".")[1])

        # Check if case exists
        case = self.bot.db.cases.find_one({"id": case_id})
        if case is None:
            await interaction.response.send_message(embed=ErrorEmbed(f"{interaction.user.mention} 找不到這個案件"),
                                                    delete_after=3,
                                                    ephemeral=True)
            return

        # Check if the use trying to accpet the case the case's wanted-assignee.
        if not interaction.user.id == case["assignee"] and case["assignee"] is not None:
            message = "你不是這個案件的預期受理人，確定要審理這個案件嗎？"
        else:
            message = "確定要審理這個案件嗎？"

        # Confirm
        await interaction.response.send_message(content=message,
                                                ephemeral=True,
                                                components=[Button(style=disnake.ButtonStyle.success,
                                                                   label="確定",
                                                                   custom_id=f"confirm.{case_id}"),
                                                            Button(style=disnake.ButtonStyle.danger,
                                                                   label="取消",
                                                                   custom_id=f"cancel.{case_id}")])

        def check(inter):
            return inter.user.id == interaction.user.id and \
                   inter.type == disnake.InteractionType.component and \
                   inter.data.custom_id in [f"confirm.{case_id}", f"cancel.{case_id}"]

        try:
            inter = await self.bot.wait_for("interaction", check=check, timeout=60)
        except asyncio.TimeoutError:
            return
        # Update database
        result = self.bot.db.cases.find_one_and_update({"id": case_id},
                                              {"$set": {
                                                  "status": {"status": "investigation", "assignee": inter.user.id}}})
        await inter.response.edit_message(embed=SuccessEmbed("你審理了這個案件!"), components=[])
        await result["complainant"].send(
            embed=SuccessEmbed(f"你的案件已被 `<@{result['assignee']}>` 審理"))

    async def reject(self, interaction):
        if not await has_admin(member=interaction.user):
            await interaction.response.send_message(embed=ErrorEmbed(f"{interaction.user.mention} 你沒有權限使用這個按鈕"),
                                                    ephemeral=True)
            return
        # Confirm
        await interaction.response.send_message(content="確定要移除這個案件嗎？",
                                                ephemeral=True,
                                                components=[Button(style=disnake.ButtonStyle.success,
                                                                   label="確定",
                                                                   custom_id=f"confirm.{interaction.message.id}"),
                                                            Button(style=disnake.ButtonStyle.danger,
                                                                   label="取消",
                                                                   custom_id=f"cancel.{interaction.message.id}")])

        def check(inter):
            return inter.user.id == interaction.user.id and \
                   inter.type == disnake.InteractionType.component and \
                   inter.data.custom_id in [f"confirm.{interaction.message.id}", f"cancel.{interaction.message.id}"]

        try:
            inter = await self.bot.wait_for("interaction", check=check, timeout=60)
        except asyncio.TimeoutError:
            return
        # Update database
        result = self.bot.db.cases.find_one_and_delete({"id": interaction.message.id})
        await interaction.message.delete()
        await inter.response.edit_message(embed=SuccessEmbed("你移除了這個案件！"), components=[])
        user = await self.bot.getch_user(result["complainant"])
        await user.send(embed=ErrorEmbed(f"你的案件已被 {inter.user.mention} 移除"))


def setup(bot):
    bot.add_cog(Buttons(bot))
