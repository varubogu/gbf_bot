from sqlalchemy import Row, select
from models.model_base import ModelBase, SessionLocal


class DbLoader():

    async def load(
            self,
            session: SessionLocal,
            table_cls: ModelBase
    ) -> [Row]:
        result = session.execute(select(table_cls))
        data = result.fetchall()
        return data
