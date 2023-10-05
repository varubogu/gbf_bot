import os

import gspread
import discord
from discord.ext import commands
from discord import app_commands
from sqlalchemy import select

from cogs.sync.gspread_base import GSpreadBase


class GSpreadPush(GSpreadBase):

    def __init__(self, bot: commands.Bot):
        self.base = super()
        self.base.__init__(
            bot,
            book_url=os.environ.get('GSPREAD_BOOK_PUSH_URL'),
            init_message="スプレッドシートにデータ書き込み中...",
            complete_message="スプレッドシートにデータ書き込み完了",
            error_message="スプレッドシートにデータ書き込み失敗",
            table_io=['out']
        )

    @app_commands.command(
            name="gspread_push",
            description="スプレッドシートへデータ書き込み"
    )
    @commands.has_role("Bot Control")
    async def command_execute(self, interaction: discord.Interaction):
        await self.base.command_execute(interaction)

    async def before_message(
            self,
            sheet_name: str
    ) -> str:
        return f"{sheet_name} push..."

    async def do(
            self,
            session,
            worksheet: gspread.Worksheet,
            cls,
            table_info
    ):

        worksheet.resize(rows=2)

        result = session.execute(select(cls))
        data = result.fetchall()

        if not data:
            return

        column_names = [column.name for column in cls.__table__.columns]

        rows = []
        for table in data:
            cells = ["" for _ in range(len(column_names))]
            for row in table:
                for attribute in dir(row):
                    if attribute not in column_names:
                        continue
                    cell = getattr(row, attribute)
                    index = column_names.index(attribute)
                    if hasattr(cell, 'strftime'):
                        cells[index] = cell.strftime('%Y-%m-%d %H:%M:%S')
                    else:
                        cells[index] = cell
            rows.append(cells)

        worksheet.append_rows(rows)


async def setup(bot: commands.Bot):
    await bot.add_cog(GSpreadPush(bot))
