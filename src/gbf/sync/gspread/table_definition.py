from gbf.models import TableNameMapping


class GSpreadTableDefinition:
    def __init__(
            self,
            table_name_jp: str = None,
            table_name_en: str = None,
            table_scope: str = None,
            table_io: str = None,
            table_metadata: dict[str, str] = None
    ):
        self.table_name_jp: str = None
        self.table_name_en: str = None
        self.table_scope: str = None
        self.table_io: str = None
        self.table_metadata: dict[str, str] = None
        self.table_cls: type = None

        if table_metadata is not None:
            self.table_metadata = table_metadata
            self.table_name_jp = table_metadata['table_name_jp']
            self.table_name_en = table_metadata['table_name_en']
            self.table_scope = table_metadata['table_scope']
            self.table_io = table_metadata['table_io']

        if table_name_jp:
            self.table_name_jp = table_name_jp

        if table_name_en:
            self.table_name_en = table_name_en

        if table_scope:
            self.table_scope = table_scope

        if table_io:
            self.table_io = table_io

        if self.table_name_en is None:
            raise ValueError(
                'table_name_en is required. '
                f'table_name_jp: {self.table_name_jp}'
            )

        if self.table_name_jp is None:
            raise ValueError(
                'table_name_en is required. '
                f'table_name_en: {self.table_name_en}'
            )

        if self.table_scope is None:
            raise ValueError(
                'table_name_en is required. '
                f'table_name_en: {self.table_name_en}'
            )

        if self.table_io is None:
            raise ValueError(
                'table_name_en is required. '
                f'table_name_en: {self.table_name_en}'
            )

        self.table_cls = TableNameMapping.getClassObject(self.table_name_en)
        if self.table_cls is None:
            raise ValueError(
                f'table_cls is None. table_name_en: {self.table_name_en}'
            )
