
import discord
from discord import app_commands
from discord.ext import commands


class Belial(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="beli", description="ベリアル募集")
    async def belial(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            "ベリアル参加者を募集します。\n"
            )
        message = await interaction.original_response()
        reactions = [
            '✅'
        ]
        for reaction in reactions:
            await message.add_reaction(reaction)

    @app_commands.command(name="beli6", description="ベリアル６属性募集")
    async def belial_six_element(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            "ベリアル参加者を募集します。\n"
            "参加属性を選んでください"
        )
        message = await interaction.original_response()
        reactions = [
            '🔴',
            '🔵',
            '🟤',
            '🟢',
            '🟡',
            '🟣',
        ]
        for reaction in reactions:
            await message.add_reaction(reaction)


async def setup(bot: commands.Bot):
    await bot.add_cog(Belial(bot))
