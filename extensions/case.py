import os

import disnake
from disnake.ext import commands

from utils import ErrorEmbed


class Case(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="case", description="案件管理", guild_ids=[921645783915319316], options=[disnake.Option(name="子指令", type=disnake.OptionType.sub_command)])
    async def case(self, interaction):
        await interaction.response.send_message(
            embed=ErrorEmbed(f"在聊天欄輸入 `/` 來查看所有可用指令，\n或前往{os.getenv('BELL_CHANNEL')} 查看說明"))

    @case.sub_command(name="list", description="列出你的案件")
    async def list(self, interaction):
        """列出你的案件"""
        await interaction.response.defer()
        cases = self.bot.db.cases.find_many({
            "$or": [
                {"complainant": interaction.author.id},
                {"assignee": interaction.author.id}
            ]
        })
        embed = disnake.Embed(title="案件列表", color=disnake.Colour.blue())
        if cases is None:
            embed.description = "你沒有任何案件"
            await interaction.response.send(embed=embed, ephemeral=True)
            return
        for case in cases:
            if case["complainant"] == interaction.author.id:
                title = "告訴📤"
            elif case["assignee"] == interaction.author.id:
                title = "審理📥"

            match case["status"]["status"]:
                case "pending":
                    status = "等待審理"
                case "investigation":
                    status = "雙方調查中"
                case "court":
                    status = "等待開庭"
                case "ended":
                    status = "已結案"
            if case["status"]["appeal"]:
                status += "(上訴)"

            content = f"""
                    **案件ID**: {case["id"]}
                    **狀態**: {status}
                    **原因**: ```{case["reason"]}``` 
                    """
            embed.add_field(name=title, value=content, inline=False)
        await interaction.response.send(embed=embed, ephemeral=True)


def setup(bot):
    bot.add_cog(Case(bot))
