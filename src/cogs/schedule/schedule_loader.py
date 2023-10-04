import discord
from discord.ext import commands
from discord import app_commands

from models.base import SessionLocal


class ScheduleLoader(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="schedule_reload", description="スケジュール再読み込み")
    @commands.has_role("Bot Control")
    async def schedule_reload(self, interaction: discord.Interaction):

        with SessionLocal() as session:
            self.schedule_delete(session)
            self.schedule_create(session)

    async def schedule_delete(self, session):
        pass

    async def schedule_create(self, session):
        pass


async def setup(bot: commands.Bot):
    await bot.add_cog(ScheduleLoader(bot))
