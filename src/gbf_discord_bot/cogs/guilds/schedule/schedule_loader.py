import traceback
import discord
from discord.ext import commands
from discord import app_commands

from gbf.models.session import AsyncSessionLocal
from gbf.schedules.manager import ScheduleManager


class ScheduleLoader(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="schedule_reload", description="スケジュール再読み込み")
    @app_commands.checks.has_role("gbf_bot_control")
    async def schedule_reload(self, interaction: discord.Interaction):

        await interaction.response.defer()
        await interaction.followup.send("スケジュール再読み込み中...")

        try:

            async with AsyncSessionLocal() as session:
                register = ScheduleManager()
                await register.event_schedule_clear(session)
                await register.event_schedule_create(session)
                await session.commit()

            await interaction.followup.send("スケジュール再読み込み完了")
        except Exception as e:
            await interaction.followup.send("スケジュール再読み込み失敗")
            print(e)
            print("Exception Type:", type(e))
            print("Exception Message:", e)
            print("Exception Args:", e.args)
            print("Traceback:")
            traceback.print_exc()
            raise


async def setup(bot: commands.Bot):
    await bot.add_cog(ScheduleLoader(bot))
