from datetime import datetime
import uuid
from sqlalchemy import UUID, BigInteger, Column, DateTime, String, and_, text
from sqlalchemy.future import select
from models.model_base import ModelBase


class Schedules(ModelBase):
    """スケジュール情報

    Args:
        Base (_type_): _description_
    """
    __tablename__ = 'schedules'
    row_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    parent_schedule_id = Column(
        UUID(as_uuid=True), nullable=True, default=None)
    parent_schedule_detail_id = Column(
        UUID(as_uuid=True), nullable=True, default=None)
    schedule_datetime = Column(DateTime)
    guild_id = Column(BigInteger)
    channel_id = Column(BigInteger)
    message_id = Column(String)

    async def insert(self, session):
        await session.add(self)

    async def delete(self, session):
        await session.delete(self)

    @classmethod
    async def bulk_insert(cls, session, schedules):
        session.add_all(schedules)

    @classmethod
    async def truncate(cls, session):
        await session.execute(text('TRUNCATE schedules'))
        await session.commit()

    @classmethod
    async def select_sinse_last_time(
            cls, session, last_time: datetime, now: datetime
    ) -> ['Schedules']:
        result = await session.execute(
            select(Schedules).filter(
                and_(
                    last_time < Schedules.schedule_datetime,
                    Schedules.schedule_datetime <= now
                )
            )
        )
        return result.scalars().all()

    @classmethod
    async def select_all(cls, session) -> ['Schedules']:
        result = await session.execute(
            select(Schedules)
        )
        return result.scalars().all()
