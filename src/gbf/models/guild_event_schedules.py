import uuid
from typing import Sequence

from sqlalchemy import (
    UUID,
    BigInteger,
    Column,
    DateTime,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from gbf.models.model_base import ModelBase
from gbf.models.table_scopes import TableScopes
from gbf.models.table_types import TableType


class GuildEventSchedules(ModelBase):
    """サーバー毎のイベントスケジュール情報

    Args:
        Base (_type_): _description_
    """
    __tablename__ = 'guild_event_schedules'
    __tabletype__ = TableType.Reference
    __tablescope__ = TableScopes.Guild
    __table_args__ = (
        UniqueConstraint(
            'event_type',
            'event_count',
            'guild_id',
            name='unique_guild_event'
        ),
        {'comment': 'サーバー毎のイベントスケジュール情報'}
    )
    
    row_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, comment="行ID")
    guild_id = Column(BigInteger, primary_key=True, comment="サーバーID")
    event_type = Column(String, comment="イベント種類")
    event_count = Column(BigInteger, comment="イベント開催回数")
    profile = Column(String, comment="(guild)イベントスケジュール詳細との紐づけプロファイル")
    weak_attribute = Column(Integer, comment="有利属性")
    start_at = Column(DateTime, comment="開始日")
    end_at = Column(DateTime, comment="終了日")



    async def create(self, session: AsyncSession):
        session.add(self)
        await session.commit()

    @classmethod
    async def select_all(
        cls,
        session: AsyncSession,
        guild_id: int
    ) -> Sequence['GuildEventSchedules']:
        """
        ギルドイベントスケジュールを全て取得する
        Args:
            session (Session): DB接続セッション
            guild_id (int): ギルドID
        Returns:
            list[GuildEventSchedules]: ギルドイベントスケジュールのリスト
        """
        result = await session.execute(
            select(cls).filter(cls.guild_id == guild_id)
        )
        return result.scalars().all()

    @classmethod
    async def select_global_all(
        cls,
        session: AsyncSession
    ) -> Sequence['GuildEventSchedules']:
        """
        ギルドイベントスケジュールを全て取得する
        Args:
            session (Session): DB接続セッション
            guild_id (int): ギルドID
        Returns:
            list[GuildEventSchedules]: ギルドイベントスケジュールのリスト
        """
        result = await session.execute(
            select(cls)
        )
        return result.scalars().all()
