
import os
from datetime import datetime
import uuid

from gbf.sync.gspread.core import GSpreadCore


class GoogleSpreadRegister:

    def __init__(self):
        book_url = os.environ.get('GSPREAD_BOOK_PUSH_URL')
        self.core = GSpreadCore(book_url)

    async def open(self):
        self.core.open()

    async def regist(self, data, worksheet, column_names):

        # データクリア
        worksheet.resize(rows=2)

        if not data:
            return

        rows = []
        for table in data:
            cells = ["" for _ in range(len(column_names))]
            for row in table:
                row_property_names = dir(row)
                for property_name in row_property_names:
                    if property_name not in column_names:
                        continue
                    cell = getattr(row, property_name)
                    index = column_names.index(property_name)
                    cells[index] = await self.convert_cell(cell)

            rows.append(cells)

        worksheet.append_rows(rows)

    async def convert_cell(cell):
        if isinstance(cell, datetime):
            return cell.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(cell, uuid.UUID):
            return str(cell)
        else:
            return cell
