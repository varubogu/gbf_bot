import discord
from discord.ext import commands
from discord import app_commands
from gbf.environment.environment_singleton import EnvironmentSingleton
from gbf.models.model_base import AsyncSessionLocal


class EnvironLoad(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.init_message = "環境変数読み込み中..."
        self.complete_message = "環境変数読み込み完了"
        self.error_message = "環境変数読み込み失敗"

    @app_commands.command(
            name="environ_load",
            description="環境変数読み込み"
    )
    @commands.has_role("Bot Control")
    async def command_execute(self, interaction: discord.Interaction):
        try:
            await interaction.response.defer()
            await interaction.followup.send(self.init_message)
            await self.execute(interaction)
            await interaction.followup.send(self.complete_message)
        except Exception as e:
            await interaction.followup.send(self.error_message)
            print(e)
            raise

    async def execute(self, interaction: discord.Interaction):
        env = EnvironmentSingleton()
        v1 = await env.get("ROLL_LEADER")
        print(v1)
        async with AsyncSessionLocal() as session:
            await env.load_db(session)
        v1 = await env.get("ROLL_LEADER")
        print(v1)


async def setup(bot: commands.Bot):
    await bot.add_cog(EnvironLoad(bot))
