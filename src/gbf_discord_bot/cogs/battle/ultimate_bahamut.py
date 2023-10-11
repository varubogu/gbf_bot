
import discord
from discord import app_commands
from discord.ext import commands
from gbf_discord_bot.cogs.battle.base_battle_recruiment_cog \
    import BaseBattleRecruitmentCog
from gbf_discord_bot.cogs.battle.target_enum import Target


class UltimateBahamut(BaseBattleRecruitmentCog):

    def __init__(self, bot: commands.Bot):
        super().__init__(bot, Target.ULTIMATE_BAHAMUT)

    @app_commands.command(name="albh", description="アルバハH募集")
    async def albh(self, interaction: discord.Interaction):
        await super().recruitment(interaction)


async def setup(bot: commands.Bot):
    await bot.add_cog(UltimateBahamut(bot))
