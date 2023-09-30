
import discord
from discord import app_commands
from discord.ext import commands
from sqlalchemy.orm import Session
from models.base import SessionLocal
from models.battle_recruitment import BattleRecruitment
from datetime import datetime, timedelta
from .target_enum import Target


class Beelzebub(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="bub", description="ベルゼバブ募集")
    async def beelzebub(self, interaction: discord.Interaction):
        await interaction.response.send_message("ベルゼバブ参加者を募集します。")
        message = await interaction.original_response()
        reactions = [
            '✅'
        ]
        for reaction in reactions:
            await message.add_reaction(reaction)

        record = BattleRecruitment()
        record.guild_id = message.guild.id
        record.channel_id = message.channel.id
        record.message_id = message.id
        record.expiry_date = datetime.now() + timedelta(days=7)
        record.battle_id = Target.BEELZEBUB.value

        with SessionLocal() as session:
            session.add(record)
            session.commit()
            session.close()

    @commands.cog.listener()
    async def add_reaction(self):
        pass


async def setup(bot: commands.Bot):
    await bot.add_cog(Beelzebub(bot))
