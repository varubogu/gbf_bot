from datetime import datetime
import uuid
import pytest
from gbf.sync.gspread.register import GSpreadRegister


class TestUnitGspreadRegister:

    @pytest.mark.asyncio
    async def test_convert_cell_int(self):
        register = GSpreadRegister()

        cell = await register.convert_cell(1)
        assert cell == 1 and type(cell) is int

    @pytest.mark.asyncio
    async def test_convert_cell_str(self):
        register = GSpreadRegister()

        cell = await register.convert_cell('1')
        assert cell == '1' and type(cell) is str

    @pytest.mark.asyncio
    async def test_convert_cell_datetime(self):
        register = GSpreadRegister()

        dt = datetime(2023, 12, 31, 23, 59, 59)
        dt_str = dt.strftime('%Y-%m-%d %H:%M:%S')
        cell = await register.convert_cell(dt)
        assert cell == dt_str and type(cell) is str

    @pytest.mark.asyncio
    async def test_convert_cell_uuid(self):
        register = GSpreadRegister()

        uuid_value = uuid.uuid4()
        uuid_str = str(uuid_value)
        cell = await register.convert_cell(uuid_value)
        assert cell == uuid_str and type(cell) is str
