import pytest
from gbf.models.environments import Environments
from gbf.sync.gspread.loader import GSpreadLoader
# from sqlalchemy import Column, String


class TestIntegrationGSpreadLoader():

    @pytest.fixture()
    def loader(self) -> GSpreadLoader:
        return GSpreadLoader()

    @pytest.fixture()
    def table_cls(self) -> Environments:
        return Environments()

    @pytest.mark.asyncio
    async def test_convert_table(self, loader):
        pass

    @pytest.mark.asyncio
    async def test_convert_value_row(self, loader, table_cls):
        pass
        # row = {
        #     'key': 'TEST_KEY1',
        #     'value': 'TEST_VALUE1',
        #     'memo': 'TEST_MEMO1'
        # }
        # columns_dict = await loader.get_columns_dict(table_cls)
        # actual = await loader.convert_row(row, columns_dict, table_cls)
        # assert actual == row

    @pytest.mark.asyncio
    async def test_get_columns_dict(self, loader, table_cls):
        pass
        # expected = {
        #     "key": Column(String, primary_key=True),
        #     "value": Column(String),
        #     "memo": Column(String)
        # }

        # actual = await loader.get_columns_dict(table_cls)
        # assert actual == expected
