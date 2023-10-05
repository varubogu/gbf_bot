import os
import discord

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from discord.ext import commands
from models import TableNameMapping

from models.base import SessionLocal


class GSpreadBase(commands.Cog):

    def __init__(
            self,
            bot: commands.Bot,
            book_url: str,
            init_message: str,
            complete_message: str,
            error_message: str,
            table_io: [str]
    ):
        self.bot = bot
        self._book_url = book_url
        self._init_message = init_message
        self._complete_message = complete_message
        self._error_message = error_message
        self._table_io = table_io

        # このクラスで生成するもの
        self._gc = None
        self._book = None
        self._all_table_metadata = None

    async def command_execute(self, interaction: discord.Interaction):
        try:
            await interaction.response.defer()
            await interaction.followup.send(self._init_message)
            await self.execute(interaction)
            await interaction.followup.send(self._complete_message)
        except Exception:
            await interaction.followup.send(self._error_message)
            raise

    async def execute(self, interaction: discord.Interaction):
        with SessionLocal() as session:

            await self.gspread_connect()
            await self.get_all_table_metadata()

            for table_info in self._all_table_metadata:
                sheet_name = table_info.get('table_name_jp')
                table_name_en = table_info.get('table_name_en')
                table_io = table_info.get('table_io')

                worksheet = self._book.worksheet(sheet_name)
                cls = TableNameMapping.getClassObject(table_name_en)

                if table_io in self._table_io:
                    m = await self.before_message(sheet_name)
                    await interaction.followup.send(m)
                    await self.do(session, worksheet, cls, table_info)

    async def gspread_connect(self):
        # Google Sheets API setup
        scope = [
            'https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive'
        ]
        credentials_path = '../gcp-credentials.json'
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            credentials_path,
            scope
        )

        self._gc = gspread.authorize(credentials)
        self._book = self._gc.open_by_url(self._book_url)

    async def get_all_table_metadata(self):
        table_name_sheet_name = os.environ.get(
            'GSPREAD_TABLE_NAME_SHEET_NAME'
        )
        table_name_worksheet = self._book.worksheet(table_name_sheet_name)
        self._all_table_metadata = table_name_worksheet.get_all_records()

    async def before_message(
            self,
            table_name_jp: str
    ) -> str:
        NotImplementedError

    async def do(
            self,
            session,
            worksheet: gspread.Worksheet,
            cls,
            table_info
    ):
        NotImplementedError
