import discord
from discord.ext import commands
from discord import app_commands

from gbf.sync.db.register import DbRegister
from gbf.sync.gspread.loader import GSpreadLoader
from models.model_base import SessionLocal
from models.util.get_column_names import get_column_names


class GSpreadLoad(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.init_message = "スプレッドシートからデータ読み込み中..."
        self.complete_message = "スプレッドシートからデータ読み込み完了"
        self.error_message = "スプレッドシートからデータ読み込み失敗"

    @app_commands.command(
            name="gspread_load",
            description="スプレッドシートからデータ読み込み"
    )
    @commands.has_role("Bot Control")
    async def command_execute(self, interaction: discord.Interaction):
        try:
            await interaction.response.defer()
            await interaction.followup.send(self.init_message)
            await self.execute(interaction)
            await interaction.followup.send(self.complete_message)
        except Exception:
            await interaction.followup.send(self.error_message)
            raise

    async def execute(self, interaction: discord.Interaction):
        loader = GSpreadLoader()
        await loader.open()

        register = DbRegister()

        with SessionLocal() as session:
            for table_dif in loader.core.table_difinition:

                if table_dif.table_io != 'in':
                    continue

                await interaction.followup.send(
                    f'{table_dif.table_name_jp} load...'
                )

                worksheet = loader.core.book.worksheet(table_dif.table_name_jp)
                table_model = await loader.load(worksheet, table_dif)

                if len(table_model) == 0:
                    continue

                await register.regist(session, table_model)


async def setup(bot: commands.Bot):
    await bot.add_cog(GSpreadLoad(bot))
