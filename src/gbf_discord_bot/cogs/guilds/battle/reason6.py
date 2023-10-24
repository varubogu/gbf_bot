
import discord
from discord import app_commands
from discord.ext import commands
from gbf_discord_bot.cogs.guilds.battle.base_battle_recruiment_cog \
    import BaseBattleRecruitmentCog
from gbf_discord_bot.cogs.guilds.battle.target_enum import Target
from gbf_discord_bot.cogs.guilds.battle.battle_type import BattleTypeEnum


class Reason6(BaseBattleRecruitmentCog):

    def __init__(self, bot: commands.Bot):
        super().__init__(bot, Target.REASON6)

    @app_commands.command(name="reason6", description="六色の理募集")
    async def reason6(self, interaction: discord.Interaction):
        await super().recruitment(interaction, BattleTypeEnum.ALL_ELEMENT)


async def setup(bot: commands.Bot):
    await bot.add_cog(Reason6(bot))
