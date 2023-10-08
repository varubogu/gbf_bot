import discord
from discord.ext import commands
from discord import app_commands

from gbf.sync.db.loader import DbLoader
from gbf.sync.gspread.register import GSpreadRegister
from models.model_base import SessionLocal


class GSpreadPush(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.init_message = "スプレッドシートにデータ書き込み中..."
        self.complete_message = "スプレッドシートにデータ書き込み完了"
        self.error_message = "スプレッドシートにデータ書き込み失敗"

    @app_commands.command(
            name="gspread_push",
            description="スプレッドシートへデータ書き込み"
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
        loader = DbLoader()

        register = GSpreadRegister()
        await register.open()

        with SessionLocal() as session:
            for table_dif in register.core.table_difinition:
                if table_dif.table_io != 'out':
                    continue

                await interaction.followup.send(
                    f'{table_dif.table_name_jp} push...'
                )

                table_cls = table_dif.table_cls
                data = await loader.load(session, table_cls)
                if not data:
                    continue

                sheet = register.core.book.worksheet(table_dif.table_name_jp)
                await register.regist(sheet, data, table_cls)


async def setup(bot: commands.Bot):
    await bot.add_cog(GSpreadPush(bot))
