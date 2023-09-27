
import discord
from discord import app_commands
from discord.ext import commands


class Beelzebub(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="bub", description="ベルゼバブ募集")
    async def beelzebub(
            self,
            interaction: discord.Interaction):
        await interaction.response.send_message("ベルゼバブ参加者を募集します。")


async def setup(bot: commands.Bot):
    await bot.add_cog(Beelzebub(bot))
