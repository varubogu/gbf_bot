from gbf.models.environments import Environments
from gbf.sync.gspread.table_definition import GSpreadTableDefinition
import pytest


class TestGSpreadTableDefinition:

    def test_table_definition(self):
        table_definition = GSpreadTableDefinition(
            '環境変数',
            'environments',
            'guild',
            'in',
        )

        assert table_definition.table_name_jp == '環境変数'
        assert table_definition.table_name_en == 'environments'
        assert table_definition.table_scope == 'guild'
        assert table_definition.table_io == 'in'
        assert table_definition.table_metadata is None
        assert table_definition.table_cls is Environments

    def test_table_definition_from_dict(self):

        table_info = {
            'table_name_jp': '環境変数',
            'table_name_en': 'environments',
            'table_scope': 'global',
            'table_io': 'in',
        }

        table_definition = GSpreadTableDefinition(table_metadata=table_info)

        assert table_definition.table_name_jp == '環境変数'
        assert table_definition.table_name_en == 'environments'
        assert table_definition.table_scope == 'global'
        assert table_definition.table_io == 'in'
        assert table_definition.table_metadata == table_info
        assert table_definition.table_cls == Environments

    def test_table_definition_from_dict_error(self):

        # table_name_jp key error
        with pytest.raises(KeyError):
            GSpreadTableDefinition(table_metadata={
                'table_name_j': '環境変数',
                'table_name_en': 'environments',
                'table_scope': 'global',
                'table_io': 'in',
            })

        # table_name_en key error
        with pytest.raises(KeyError):
            GSpreadTableDefinition(table_metadata={
                'table_name_jp': '環境変数',
                'table_name_e': 'environments',
                'table_scope': 'global',
                'table_io': 'in',
            })

        # table_scope key error
        with pytest.raises(KeyError):
            GSpreadTableDefinition(table_metadata={
                'table_name_jp': '環境変数',
                'table_name_en': 'environments',
                'table_scop': 'global',
                'table_io': 'in',
            })

        # table_io key error
        with pytest.raises(KeyError):
            GSpreadTableDefinition(table_metadata={
                'table_name_jp': '環境変数',
                'table_name_en': 'environments',
                'table_scope': 'global',
                'table_i': 'in',
            })
