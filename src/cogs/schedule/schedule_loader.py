import discord
from discord.ext import commands
from discord import app_commands

from models.model_base import SessionLocal
from gbf.schedules.manager import ScheduleManager


class ScheduleLoader(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="schedule_reload", description="スケジュール再読み込み")
    @commands.has_role("Bot Control")
    async def schedule_reload(self, interaction: discord.Interaction):

        await interaction.response.defer()
        await interaction.followup.send("スケジュール再読み込み中...")

        try:

            with SessionLocal() as session:
                register = ScheduleManager()
                await register.event_schedule_clear(session)
                await register.event_schedule_create(session)
                session.commit()

            await interaction.followup.send("スケジュール再読み込み完了")
        except Exception as e:
            await interaction.followup.send("スケジュール再読み込み失敗")
            raise e


async def setup(bot: commands.Bot):
    await bot.add_cog(ScheduleLoader(bot))
