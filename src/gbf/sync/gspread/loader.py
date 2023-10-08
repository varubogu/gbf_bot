import os
from gbf.sync.gspread.core import GSpreadCore
from models.model_base import ModelBase
from models.util.get_column_names import get_column_names


class GSpreadLoader():

    def __init__(self):
        book_url = os.environ.get('GSPREAD_BOOK_LOAD_URL')
        self.core = GSpreadCore(book_url)

    async def open(self):
        await self.core.open()

    async def all_load(self) -> [[ModelBase]]:

        tables = []

        for table_dif in self.core.table_difinition:

            worksheet = self.core.book.worksheet(table_dif.table_name_jp)
            table = await self.load(worksheet, table_dif)
            tables.append(table)

        return tables

    async def load(self, worksheet, table_meta) -> [ModelBase]:

        data = worksheet.get_all_records()

        # テーブル定義から列情報取得
        column_names = await get_column_names(table_meta.table_cls)

        if not data:
            return

        is_first_record = True

        rows = []
        for row in data:
            # 1行目は日本語列名のため省略する
            if is_first_record:
                is_first_record = False
                continue

            # 列名と同じキーの辞書を作成
            r = {key: (row[key]) for key in row if key in column_names}

            # 辞書をもとにクラスオブジェクトを作成
            rows.append(table_meta.table_cls(**r))

        return rows
