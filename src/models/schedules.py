from datetime import datetime
import uuid
from sqlalchemy import UUID, BigInteger, Column, DateTime, String, and_
from models.base import Base


class Schedules(Base):
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

    def insert(self, session):
        session.add(self)

    def delete(self, session):
        session.delete(self)

    @classmethod
    def bulk_insert(cls, session, schedules):
        for schedule in schedules:
            schedule.insert(session)

    @classmethod
    def truncate(cls, session):
        session.execute('TRUNCATE schedules')
        session.commit()

    @classmethod
    def select_sinse_last_time(
            cls, session, last_time: datetime, now: datetime
    ) -> ['Schedules']:
        stmt = session.query(Schedules).filter(
            and_(
                last_time < Schedules.schedule_datetime,
                Schedules.schedule_datetime <= now
            )
        )
        return stmt.all()

    @classmethod
    def select_all(cls, session) -> ['Schedules']:
        stmt = session.query(Schedules)
        return stmt.all()
