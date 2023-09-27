
import discord
from discord import app_commands
from discord.ext import commands


class Belial(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="beli", description="ベリアル募集")
    async def belial(
            self,
            interaction: discord.Interaction):
        await interaction.response.send_message("ベリアル参加者を募集します。属性を選んでください。")
        interaction_message = await interaction.original_response()
        await interaction_message.add_reaction('✅')


async def setup(bot: commands.Bot):
    await bot.add_cog(Belial(bot))
