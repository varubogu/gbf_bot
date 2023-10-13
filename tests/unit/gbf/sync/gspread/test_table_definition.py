from gbf.sync.gspread.table_definition import GSpreadTableDefinition
import pytest


class TestGSpreadTableDefinition:

    def test_table_definition(self):
        table_definition = GSpreadTableDefinition(
            '日本語名',
            'EnglishName',
            'guild',
            'in',
        )

        assert table_definition.table_name_jp == '日本語名'
        assert table_definition.table_name_en == 'EnglishName'
        assert table_definition.table_scope == 'guild'
        assert table_definition.table_io == 'in'
        assert table_definition.table_metadata is None

    def test_table_definition_from_dict(self):

        table_info = {
            'table_name_jp': '日本語名',
            'table_name_en': 'EnglishName',
            'table_scope': 'guild',
            'table_io': 'in',
        }

        table_definition = GSpreadTableDefinition(table_metadata=table_info)

        assert table_definition.table_name_jp == '日本語名'
        assert table_definition.table_name_en == 'EnglishName'
        assert table_definition.table_scope == 'guild'
        assert table_definition.table_io == 'in'
        assert table_definition.table_metadata == table_info

    def test_table_definition_from_dict_error(self):

        # table_name_jp key error
        with pytest.raises(KeyError):
            GSpreadTableDefinition(table_metadata={
                'table_name_j': '日本語名',
                'table_name_en': 'EnglishName',
                'table_scope': 'guild',
                'table_io': 'in',
            })

        # table_name_en key error
        with pytest.raises(KeyError):
            GSpreadTableDefinition(table_metadata={
                'table_name_jp': '日本語名',
                'table_name_e': 'EnglishName',
                'table_scope': 'guild',
                'table_io': 'in',
            })

        # table_scope key error
        with pytest.raises(KeyError):
            GSpreadTableDefinition(table_metadata={
                'table_name_jp': '日本語名',
                'table_name_en': 'EnglishName',
                'table_scop': 'guild',
                'table_io': 'in',
            })

        # table_io key error
        with pytest.raises(KeyError):
            GSpreadTableDefinition(table_metadata={
                'table_name_jp': '日本語名',
                'table_name_en': 'EnglishName',
                'table_scope': 'guild',
                'table_i': 'in',
            })
