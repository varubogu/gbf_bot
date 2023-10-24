
import discord
from discord import app_commands
from discord.ext import commands


class CogReload(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="reload_cog", description="cogリロード")
    @app_commands.checks.has_role("gbf_bot_control")
    async def reload_cog(
            self,
            interaction: discord.Interaction,
            cog_name: str
    ):

        await interaction.response.send_message(
            f"cog [{cog_name}] reload...",
            ephemeral=True
        )
        await self.bot.reload_extension(cog_name)
        response = await interaction.original_response()
        await response.edit(f"'{cog_name}' has been reloaded")


async def setup(bot: commands.Bot):
    await bot.add_cog(CogReload(bot))
