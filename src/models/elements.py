from sqlalchemy import Column, String, Integer
from models.model_base import ModelBase
from sqlalchemy.future import select


class Elements(ModelBase):
    """属性定義

    Args:
        Base (_type_): _description_
    """
    __tablename__ = 'elements'
    element_id = Column(Integer, primary_key=True)
    stamp = Column
    name_jp = Column(String)
    name_en = Column(String)

    @classmethod
    async def select(cls, session, element_id: int) -> 'Elements':
        result = await session.execute(
            select(cls).filter(cls.element_id == element_id))
        return result.scalars().first()
