import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials

from gbf.sync.gspread.table_definition import GSpreadTableDefinition


class GSpreadCore():
    def __init__(
            self,
            book_url: str
    ):
        self.book_url: str = book_url

        # このクラスで生成するもの
        self._gc: gspread.Client = None
        self.book: gspread.Spreadsheet = None
        self.table_difinition: list[GSpreadTableDefinition] = None

    async def open(self):
        await self._book_open()
        await self._read_table_definition()

    async def _book_open(self):
        # Google Sheets API setup
        scope = [
            'https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive'
        ]
        credentials_path = os.path.join(
            os.environ['CONFIG_FOLDER'],
            'gcp-credentials.json'
        )
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            credentials_path,
            scope
        )

        self._gc = gspread.authorize(credentials)
        self.book = self._gc.open_by_url(self.book_url)

    async def _read_table_definition(self):
        """「テーブル名」シートを読み込み、テーブル情報を作成する
        """
        definition_sheet_name = os.environ.get(
            'GSPREAD_TABLE_NAME_SHEET_NAME'
        )
        table_definition_sheet = self.book.worksheet(definition_sheet_name)
        table_definitions = table_definition_sheet.get_all_records()

        self.table_difinition = [
            GSpreadTableDefinition(table_metadata=m) for m in table_definitions
        ]
