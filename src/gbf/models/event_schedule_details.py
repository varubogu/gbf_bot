import uuid
from sqlalchemy import UUID, BigInteger, Column, String
from sqlalchemy.future import select
from gbf.models.model_base import ModelBase
from gbf.models.table_scopes import TableScopes
from gbf.models.table_types import TableType


class EventSchedulesDetails(ModelBase):
    """イベント期間内詳細スケジュール

    Args:
        Base (_type_): _description_
    """
    __tablename__ = 'event_schedules_details'
    __tabletype__ = TableType.Reference
    __tablescope__ = TableScopes.All
    row_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    profile = Column(String)
    start_day_relative = Column(String)
    time = Column(String)
    schedule_name = Column(String)
    message_id = Column(String)
    guild_id = Column(BigInteger)
    channel_id = Column(BigInteger)
    reactions = Column(String)

    async def create(self, session):
        await session.add(self)
        await session.commit()

    @classmethod
    async def select_all(cls, session):
        result = await session.execute(select(cls))
        return result.scalars().all()
