import uuid
from sqlalchemy import UUID, BigInteger, Column, String
from sqlalchemy.future import select
from gbf.models.model_base import ModelBase
from gbf.models.table_scopes import TableScopes
from gbf.models.table_types import TableType


class GuildEventSchedulesDetails(ModelBase):
    """イベント期間内詳細スケジュール

    Args:
        Base (_type_): _description_
    """
    __tablename__ = 'guild_event_schedules_details'
    __tabletype__ = TableType.Reference
    __tablescope__ = TableScopes.Guild
    row_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    guild_id = Column(BigInteger, primary_key=True)
    profile = Column(String)
    start_day_relative = Column(String)
    time = Column(String)
    schedule_name = Column(String)
    message_id = Column(String)
    channel_id = Column(BigInteger)
    reactions = Column(String)

    async def create(self, session):
        session.add(self)
        await session.commit()

    @classmethod
    async def select_all(cls, session):
        result = await session.execute(select(cls))
        return result.scalars().all()
