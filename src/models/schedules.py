from datetime import datetime
import uuid
from sqlalchemy import UUID, Column, DateTime, String, and_
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
    schedule_time = Column(DateTime)
    message_id = Column(String)
    channel_id = Column(String)

    def insert(self, session):
        session.add(self)

    def delete(self, session):
        session.delete(self)

    @classmethod
    def bulk_insert(cls, session, schedules):
        for schedule in schedules:
            schedule.insert(session)

    @classmethod
    def select_sinse_last_time(
            cls, session, last_time: datetime, now: datetime
    ) -> ['Schedules']:
        stmt = session.query(Schedules).filter(
            and_(
                last_time < Schedules.schedule_time,
                Schedules.schedule_time <= now
            )
        )
        return stmt.all()
