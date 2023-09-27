import discord
from discord import app_commands
from discord.ext import commands


class Sample(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="sample", description="テストコマンドです。")
    async def sample_command(
            self,
            interaction: discord.Interaction,
            text: str = "コマンド使用者のみのてすと"):
        await interaction.response.send_message(text, ephemeral=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(Sample(bot))
