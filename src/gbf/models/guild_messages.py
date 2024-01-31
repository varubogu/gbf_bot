from typing import Sequence
from sqlalchemy import BigInteger, Column, String, and_
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from gbf.models.model_base import ModelBase
from gbf.models.table_scopes import TableScopes
from gbf.models.table_types import TableType


class GuildMessages(ModelBase):
    """メッセージ定義

    Args:
        Base (_type_): _description_
    """
    __tablename__ = 'guild_messages'
    __tabletype__ = TableType.Reference
    __tablescope__ = TableScopes.Guild
    guild_id = Column(BigInteger, primary_key=True)
    message_id = Column(String, primary_key=True)
    message_jp = Column(String)
    reactions = Column(String)
    memo = Column(String)

    @classmethod
    async def select_single(
        cls,
        session: AsyncSession,
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
        session: AsyncSession,
        guild_id: int,
        message_ids: list[str]
    ) -> Sequence['GuildMessages']:
        result = await session.execute(
            select(cls).filter(and_(
                cls.guild_id == guild_id,
                cls.message_id.in_(message_ids)
            ))
        )
        return result.scalars().all()
