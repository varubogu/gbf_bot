import os

from sqlalchemy import BigInteger, DateTime, Integer, String, Uuid
from gbf.sync.gspread.core import GSpreadCore
from gbf.models.model_base import ModelBase
from gbf.utils.convert_datetime import convert_datetime


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
        # column_names = await get_column_names(table_meta.table_cls)

        if not data:
            return

        is_first_record = True

        rows = []
        for row in data:
            # 1行目は日本語列名のため省略する
            if is_first_record:
                is_first_record = False
                continue

            # 辞書をもとにクラスオブジェクトを作成
            r = await self.convert_object(row, table_meta)
            rows.append(r)

        return rows

    async def convert_object(self, row, table_meta):

        columns = table_meta.table_cls.__table__.columns
        r = {}
        for key in row:
            column = [c for c in columns if c.name == key]
            if not column:
                continue
            column = column[0]

            if isinstance(column.type, Integer):
                r[key] = int(row[key])
            elif isinstance(column.type, BigInteger):
                r[key] = int(row[key])
            elif isinstance(column.type, String):
                r[key] = str(row[key])
            elif isinstance(column.type, Uuid):
                r[key] = row[key]
            elif isinstance(column.type, DateTime):
                r[key] = await convert_datetime(str(row[key]))
            else:
                raise Exception("Invalid column type")

        # 辞書をもとにクラスオブジェクトを作成
        return table_meta.table_cls(**r)
