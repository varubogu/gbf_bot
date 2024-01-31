from sqlalchemy import Column, String, Integer
from gbf.models.model_base import ModelBase
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from gbf.models.table_scopes import TableScopes

from gbf.models.table_types import TableType


class Elements(ModelBase):
    """属性定義

    Args:
        Base (_type_): _description_
    """
    __tablename__ = 'elements'
    __tabletype__ = TableType.Reference
    __tablescope__ = TableScopes.All
    element_id = Column(Integer, primary_key=True)
    stamp = Column(String)
    name_jp = Column(String)
    name_en = Column(String)

    @classmethod
    async def select(cls, session: AsyncSession, element_id: int) -> 'Elements':
        result = await session.execute(
            select(cls).filter(cls.element_id == element_id))
        return result.scalars().first()
