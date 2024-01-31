from typing import Sequence
import uuid
from sqlalchemy \
    import UUID, Column, UniqueConstraint, \
    DateTime, BigInteger, Integer, String
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from gbf.models.model_base import ModelBase
from gbf.models.table_scopes import TableScopes
from gbf.models.table_types import TableType


class GuildEventSchedules(ModelBase):
    """イベントスケジュール情報

    Args:
        Base (_type_): _description_
    """
    __tablename__ = 'guild_event_schedules'
    __tabletype__ = TableType.Reference
    __tablescope__ = TableScopes.Guild
    row_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    guild_id = Column(BigInteger, primary_key=True)
    event_type = Column(String)
    event_count = Column(BigInteger)
    profile = Column(String)
    weak_attribute = Column(Integer)
    start_at = Column(DateTime)
    end_at = Column(DateTime)

    __table_args__ = (
        UniqueConstraint(
            'event_type',
            'event_count',
            'guild_id',
            name='unique_guild_event'
        ),
    )

    async def create(self, session: AsyncSession):
        session.add(self)
        await session.commit()

    @classmethod
    async def select_all(cls, session, guild_id: int) -> list['GuildEventSchedules']:
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
