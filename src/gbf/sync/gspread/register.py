
import os
from datetime import datetime
import uuid

from sqlalchemy import Row

from gbf.sync.gspread.core import GSpreadCore
from models.model_base import ModelBase
from models.util.get_column_names import get_column_names
import gspread


class GSpreadRegister:

    def __init__(self):
        book_url = os.environ.get('GSPREAD_BOOK_PUSH_URL')
        self.core = GSpreadCore(book_url)

    async def open(self):
        await self.core.open()

    async def regist(
            self,
            sheet: gspread.Worksheet,
            data: [Row],
            data_cls: ModelBase
    ):

        # データクリア
        sheet.resize(rows=2)

        if not data:
            return

        column_names = await get_column_names(data_cls)

        rows = []
        for table in data:
            cells = ["" for _ in range(len(column_names))]
            for row in table:
                row_property_names = dir(row)
                for property_name in row_property_names:
                    if property_name not in column_names:
                        continue
                    cell_value = getattr(row, property_name)
                    index = column_names.index(property_name)
                    cells[index] = await self.convert_cell(cell_value)

            rows.append(cells)

        sheet.append_rows(rows)

    async def convert_cell(self, cell_value: any):
        if isinstance(cell_value, datetime):
            return cell_value.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(cell_value, uuid.UUID):
            return str(cell_value)
        else:
            return cell_value
