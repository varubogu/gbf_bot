
import discord
from discord import app_commands
from discord.ext import commands
from gbf_discord_bot.cogs.commons.battle.base_battle_recruiment_cog \
    import BaseBattleRecruitmentCog
from gbf_discord_bot.cogs.commons.battle.target_enum import Target


class ProtoBahamutHL(BaseBattleRecruitmentCog):

    def __init__(self, bot: commands.Bot):
        super().__init__(bot, Target.PROTO_BAHAMUT_HL)

    @app_commands.command(name="tybh", description="つよバハ募集")
    async def tybh(self, interaction: discord.Interaction):
        await super().recruitment(interaction)


async def setup(bot: commands.Bot):
    await bot.add_cog(ProtoBahamutHL(bot))
