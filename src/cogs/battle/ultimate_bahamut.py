
import discord
from discord import app_commands
from discord.ext import commands


class UltimateBahamut(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name='ulbh', description='アルバハ募集')
    async def ultimate_bahamut(self, interaction: discord.Interaction):

        await interaction.response.send_message(
            '@here アルバハ参加者を募集します。'
        )
        message = await interaction.original_response()
        reactions = [
            '✅'
        ]
        for reaction in reactions:
            await message.add_reaction(reaction)


async def setup(bot: commands.Bot):
    await bot.add_cog(UltimateBahamut(bot))
