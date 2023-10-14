from datetime import datetime
import uuid
import pytest
from gbf.sync.gspread.loader import GSpreadLoader
from sqlalchemy import Column, Integer, BigInteger, String, DateTime, Uuid


class TestUnitGSpreadLoader():

    @pytest.fixture()
    def loader(self) -> GSpreadLoader:
        return GSpreadLoader()

    @pytest.mark.asyncio
    async def test_convert_value_int(self, loader):
        actual = await loader.convert_value("1", Column(Integer))
        assert actual == 1 and isinstance(actual, int)

        actual = await loader.convert_value("1", Column(BigInteger))
        assert actual == 1 and isinstance(actual, int)

    @pytest.mark.asyncio
    async def test_convert_value_str(self, loader):
        actual = await loader.convert_value("1", Column(String))
        assert actual == "1" and isinstance(actual, str)

    @pytest.mark.asyncio
    async def test_convert_value_datetime(self, loader):
        loader = GSpreadLoader()
        dt_str = "2023/12/31"
        actual = await loader.convert_value(dt_str, Column(DateTime))
        expected = datetime(2023, 12, 31)
        assert actual == expected and isinstance(actual, datetime)

        dt_str = "2023/12/31 23:59:59"
        actual = await loader.convert_value(dt_str, Column(DateTime))
        expected = datetime(2023, 12, 31, 23, 59, 59)
        assert actual == expected and isinstance(actual, datetime)

    @pytest.mark.asyncio
    async def test_convert_value_uuid(self, loader):
        actual_str = 'cdc1a3ca-6365-485c-b8e0-7e6a5d5ac5aa'
        actual = await loader.convert_value(actual_str, Column(Uuid))
        expected = uuid.UUID(actual_str)
        assert actual == expected and isinstance(actual, uuid.UUID)
