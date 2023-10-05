import os

import gspread
import discord
from discord.ext import commands
from discord import app_commands

from cogs.sync.gspread_base import GSpreadBase


class GSpreadLoad(GSpreadBase):

    def __init__(self, bot: commands.Bot):
        self.base = super()
        self.base.__init__(
            bot,
            book_url=os.environ.get('GSPREAD_BOOK_PUSH_URL'),
            init_message="スプレッドシートからデータ読み込み中...",
            complete_message="スプレッドシートからデータ読み込み完了",
            error_message="スプレッドシートからデータ読み込み失敗",
            table_io=['in']
        )

    @app_commands.command(
            name="gspread_load",
            description="スプレッドシートからデータ読み込み"
    )
    @commands.has_role("Bot Control")
    async def command_execute(self, interaction: discord.Interaction):
        await self.base.command_execute(interaction)

    async def before_message(
            self,
            sheet_name: str
    ) -> str:
        return f"{sheet_name} load..."

    async def do(
            self,
            session,
            worksheet: gspread.Worksheet,
            cls,
            table_info
    ):
        data = worksheet.get_all_records()

        column_names = [column.name for column in cls.__table__.columns]

        if not data:
            return

        is_first_record = True

        for row in data:
            # 1行目は日本語列名のため省略する
            if (is_first_record):
                is_first_record = False
                continue

            r = {key: (row[key]) for key in row if key in column_names}

            table = cls(**r)
            # column_namesの先頭から1～n列目が主キーという想定のため、1列目が空欄かで判断
            if not getattr(table, column_names[0]):
                # 主キーが空の項目は弾く
                continue

            session.merge(table)

        # テーブル単位コミット
        session.commit()


async def setup(bot: commands.Bot):
    await bot.add_cog(GSpreadLoad(bot))
