from gbf.models import ModelBase
from sqlalchemy import Column


async def get_column_names(table_cls: ModelBase) -> [str]:
    return [column.name for column in table_cls.__table__.columns]


async def get_columns(table_cls: ModelBase) -> [Column]:
    return table_cls.__table__.columns
