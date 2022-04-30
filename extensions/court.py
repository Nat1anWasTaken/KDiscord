import discord
from discord.ext import commands
from modals.accuse import Accuse


class Court(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.command(name="accuse", description="提起一個告訴")
    async def accuse(self, ctx):
        await ctx.interaction.response.send_modal(Accuse(self.bot))


def setup(bot):
    bot.add_cog(Court(bot))
