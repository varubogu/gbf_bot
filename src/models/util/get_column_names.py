from models import ModelBase


async def get_column_names(table_cls: ModelBase) -> [str]:
    return [column.name for column in table_cls.__table__.columns]
