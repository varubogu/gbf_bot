import discord
from discord.ext import commands
from discord import app_commands


class ScheduleLoader(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="schedule_reload", description="スケジュール再読み込み")
    @commands.has_role("Bot Control")
    async def schedule_reload(self, interaction: discord.Interaction):
        await interaction.response.send_message('ok')


async def setup(bot: commands.Bot):
    await bot.add_cog(ScheduleLoader(bot))
