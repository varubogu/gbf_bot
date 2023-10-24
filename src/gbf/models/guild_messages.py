from sqlalchemy import BigInteger, Column, String, and_
from sqlalchemy.future import select
from gbf.models.model_base import ModelBase


class GuildMessages(ModelBase):
    """メッセージ定義

    Args:
        Base (_type_): _description_
    """
    __tablename__ = 'messages'
    guild_id = Column(BigInteger, primary_key=True)
    message_id = Column(String, primary_key=True)
    message_jp = Column(String)
    reactions = Column(String)
    memo = Column(String)

    @classmethod
    async def select_one(
        cls,
        session,
        guild_id: int,
        message_id: str
    ) -> 'GuildMessages':
        result = await session.execute(
            select(cls).filter(and_(
                cls.guild_id == guild_id,
                cls.message_id == message_id
            ))
        )
        return result.scalars().first()

    @classmethod
    async def select_multi(
        cls,
        session,
        guild_id: int,
        message_ids: [str]
    ) -> ['GuildMessages']:
        result = await session.execute(
            select(cls).filter(and_(
                cls.guild_id == guild_id,
                cls.message_id.in_(message_ids)
            ))
        )
        return result.scalars().all()
