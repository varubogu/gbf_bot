import os
from typing import Any
from uuid import UUID

from sqlalchemy import BigInteger, Column, DateTime, Integer, String, Uuid
from gbf.sync.gspread.core import GSpreadCore
from gbf.models.model_base import ModelBase
from gbf.sync.gspread.table_definition import GSpreadTableDefinition
from gbf.utils.convert_datetime import convert_datetime


class GSpreadLoader():

    def __init__(self):
        book_url = os.environ.get('GSPREAD_BOOK_LOAD_URL')
        self.core = GSpreadCore(book_url)

    async def open(self):
        await self.core.open()

    async def convert_table(
            self,
            data: list[dict[str, Any]],
            table_difinition: GSpreadTableDefinition
    ) -> list[ModelBase]:
        """スプレッドシートから読み込んだシートデータをテーブルデータに変換する

        Args:
            data (list[dict[str, Any]]): スプレッドシートから読み込んだシートデータ
            table_difinition (GSpreadTableDefinition): テーブル定義情報

        Returns:
            list[ModelBase]: テーブルデータ変換後のデータ
        """

        if not data:
            return

        is_first_record = True

        rows = []

        table_cls = table_difinition.table_cls
        columns = self.get_columns_dict(table_cls)

        for row in data:
            # 1行目は日本語列名のため省略する
            if is_first_record:
                is_first_record = False
                continue

            # 辞書をもとにクラスオブジェクトを作成
            r = await self.convert_row(row, columns, table_cls)
            rows.append(r)

        return rows

    async def convert_row(
            self,
            row: dict[str, Any],
            columns_dict: dict[str, Column],
            table_cls: type
    ) -> ModelBase:
        """スプレッドシートの行をインスタンスに変換する

        Args:
            row (dict[str, Any]): スプレッドシートの行情報
            columns_dict (dict[str, Column]): 列名と列定義の辞書
            table_difinition (GSpreadTableDefinition): テーブル定義情報

        Returns:
            ModelBase: テーブル定義オブジェクト
        """
        row_dict = {}
        for col_name in row:

            column = columns_dict.get(col_name)
            if column is None:
                print(f'Invalid column name. "{col_name}"')
                continue

            value = row[col_name]

            row_dict[col_name] = await self.convert_value(value, column)

        # 辞書をもとにクラスオブジェクトを作成
        return table_cls(**row_dict)

    async def convert_value(
            self,
            cell_value: Any,
            column: Column
    ):
        """sqlalchemy.Columnの定義をもとに値を変換する
        対応型：Integer, BigInteger, String, Uuid, DateTime

        Args:
            cell_value (Any): セルの値
            column (Column): sqlalchemyの列定義

        Raises:
            Exception: 列の型が動作対象外

        Returns:
            Any: 型変換後の値
        """
        if isinstance(column.type, Integer):
            return int(cell_value)
        elif isinstance(column.type, BigInteger):
            return int(cell_value)
        elif isinstance(column.type, String):
            return str(cell_value)
        elif isinstance(column.type, Uuid):
            return UUID(cell_value)
        elif isinstance(column.type, DateTime):
            return await convert_datetime(cell_value)
        else:
            raise ValueError("Invalid column type")

    async def get_columns_dict(
            self,
            table_cls: type
    ) -> dict[str, Column]:
        """テーブルカラム情報の辞書を作成する

        Args:
            table_cls (type): テーブルクラス

        Returns:
            dict[str, Column]: key: テーブル列名 value:テーブルクラスのカラム情報
        """
        return {c.name: c for c in table_cls.__table__.columns}
