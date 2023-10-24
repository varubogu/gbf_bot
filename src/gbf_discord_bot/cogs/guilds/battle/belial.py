
import discord
from discord import app_commands
from discord.ext import commands
from gbf_discord_bot.cogs.guilds.battle.base_battle_recruiment_cog \
    import BaseBattleRecruitmentCog
from gbf_discord_bot.cogs.guilds.battle.target_enum import Target
from gbf_discord_bot.cogs.guilds.battle.battle_type import BattleTypeEnum


class Belial(BaseBattleRecruitmentCog):

    def __init__(self, bot: commands.Bot):
        super().__init__(bot, Target.BELIAL)

    @app_commands.command(name="beli", description="ベリアル募集")
    async def beli(self, interaction: discord.Interaction):
        await super().recruitment(interaction)

    @app_commands.command(name="beli6", description="ベリアル６属性募集")
    async def beli_all_element(self, interaction: discord.Interaction):
        await super().recruitment(interaction, BattleTypeEnum.ALL_ELEMENT)


async def setup(bot: commands.Bot):
    await bot.add_cog(Belial(bot))
