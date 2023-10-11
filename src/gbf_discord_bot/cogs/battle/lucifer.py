
import discord
from discord import app_commands
from discord.ext import commands
from gbf_discord_bot.cogs.battle.base_battle_recruiment_cog \
    import BaseBattleRecruitmentCog
from gbf_discord_bot.cogs.battle.target_enum import Target
from gbf_discord_bot.cogs.battle.battle_type import BattleTypeEnum


class Lucifer(BaseBattleRecruitmentCog):

    def __init__(self, bot: commands.Bot):
        super().__init__(bot, Target.LUCIFER)

    @app_commands.command(name="luci", description="ルシH募集")
    async def luci(self, interaction: discord.Interaction):
        await super().recruitment(interaction)

    @app_commands.command(name="luci6", description="ルシH6属性募集")
    async def luci_all_element(self, interaction: discord.Interaction):
        await super().recruitment(interaction, BattleTypeEnum.ALL_ELEMENT)


async def setup(bot: commands.Bot):
    await bot.add_cog(Lucifer(bot))
