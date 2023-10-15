import pytest
from sqlalchemy import Column, String
from gbf.models.environments import Environments
from gbf.sync.gspread.loader import GSpreadLoader
from gbf.sync.gspread.table_definition import GSpreadTableDefinition


class TestIntegrationGSpreadLoader():

    @pytest.fixture()
    def loader(self) -> GSpreadLoader:
        return GSpreadLoader()

    @pytest.fixture()
    def table_cls(self):
        return Environments

    @pytest.fixture()
    def table_instance(self) -> Environments:
        return Environments()

    @pytest.mark.asyncio
    async def test_convert_table(
        self,
        loader: GSpreadLoader,
        async_db_session
    ):
        table_dif = GSpreadTableDefinition(
            table_name_jp="環境変数",
            table_name_en="environments",
            table_scope="global",
            table_io="in"
        )

        data = [
            {
                "key": "先頭行は日本語列名のため無視される",
                "value": "先頭行は日本語列名のため無視される",
                "memo": "先頭行は日本語列名のため無視される"
            },
            {
                "key": "TEST1KEY",
                "value": "TEST1VALUE",
                "memo": "TEST1MEMO"
            },
            {
                "key": "TEST2KEY",
                "value": "TEST2VALUE",
                "memo": "TEST2MEMO"
            }
        ]

        actual_list = await loader.convert_table(data, table_dif)
        actual_count = len(actual_list)
        expected_count = len(data) - 1  # dataの先頭行は無視されるため-1
        assert actual_count == expected_count
        for i in range(actual_count):
            # dataの先頭行は無視されるためインデックス+1
            assert actual_list[i].key == data[i+1].get("key")
            assert actual_list[i].value == data[i+1].get("value")
            assert actual_list[i].memo == data[i+1].get("memo")

    @pytest.mark.asyncio
    async def test_convert_value_row(
        self,
        loader: GSpreadLoader,
        table_cls
    ):
        row = {
            "key": "TEST1KEY",
            "value": "TEST1VALUE",
            "memo": "TEST1MEMO"
        }
        columns_dict = await loader.get_columns_dict(table_cls)
        actual = await loader.convert_row(row, columns_dict, table_cls)
        assert isinstance(actual, Environments)
        assert actual.key == row["key"]
        assert actual.value == row["value"]
        assert actual.memo == row["memo"]

    @pytest.mark.asyncio
    async def test_get_columns_dict(
        self,
        loader: GSpreadLoader,
        table_instance: Environments
    ):
        expected = {
            "key": Column(String, primary_key=True),
            "value": Column(String),
            "memo": Column(String)
        }

        actual = await loader.get_columns_dict(table_instance)
        assert len(actual) == len(expected)
        for name in actual:
            assert expected.get(name) is not None
