from sqlalchemy import Row, select
from sqlalchemy.ext.asyncio import AsyncSession
from models.model_base import ModelBase


class DbLoader():

    async def load(
            self,
            session: AsyncSession,
            table_cls: ModelBase
    ) -> [Row]:
        result = await session.execute(select(table_cls))
        data = result.fetchall()
        return data
