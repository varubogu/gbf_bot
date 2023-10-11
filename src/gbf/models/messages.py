from sqlalchemy import Column, String
from sqlalchemy.future import select
from gbf.models.model_base import ModelBase


class Messages(ModelBase):
    """メッセージ定義

    Args:
        Base (_type_): _description_
    """
    __tablename__ = 'messages'
    message_id = Column(String, primary_key=True)
    message_jp = Column(String)
    reactions = Column(String)
    memo = Column(String)

    @classmethod
    async def select_one(cls, session, message_id: str) -> 'Messages':
        result = await session.execute(
            select(cls).filter(cls.message_id == message_id)
        )
        return result.scalars().first()

    @classmethod
    async def select_multi(cls, session, message_ids: [str]) -> ['Messages']:
        result = await session.execute(
            select(cls).filter(cls.message_id.in_(message_ids))
        )
        return result.scalars().all()
