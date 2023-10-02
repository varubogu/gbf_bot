
import discord
from discord import app_commands
from discord.ext import commands
from cogs.battle.base_battle_recruiment_cog import BaseBattleRecruitmentCog
from cogs.battle.target_enum import Target
from cogs.battle.battle_type import BattleTypeEnum


class SuperUltimateBahamut(BaseBattleRecruitmentCog):

    def __init__(self, bot: commands.Bot):
        super().__init__(bot, Target.SUPER_ULTIMATE_BAHAMUT)

    @app_commands.command(name="spbh6", description="スパバハ６属性募集")
    async def spbh6(self, interaction: discord.Interaction):
        await super().recruitment(interaction, BattleTypeEnum.ALL_ELEMENT)


async def setup(bot: commands.Bot):
    await bot.add_cog(SuperUltimateBahamut(bot))
