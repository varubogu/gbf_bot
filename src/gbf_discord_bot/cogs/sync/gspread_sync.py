import discord
from discord.ext import commands
from discord import app_commands

from gbf_discord_bot.cogs.sync.gspread_load import GSpreadLoad
from gbf_discord_bot.cogs.sync.gspread_push import GSpreadPush


class GSpreadSync(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
            name="gspread_sync",
            description="スプレッドシートとデータ同期（load & push)"
    )
    @commands.has_role("Bot Control")
    async def gspread_sync(self, interaction: discord.Interaction):

        await interaction.response.defer()
        await GSpreadLoad.gspread_load(interaction)
        await GSpreadPush.gspread_push(interaction)


async def setup(bot: commands.Bot):
    await bot.add_cog(GSpreadSync(bot))
