import uuid
from sqlalchemy import UUID, Column, String
from models.base import Base


class EventSchedulesDetail(Base):
    """イベント期間内詳細スケジュール

    Args:
        Base (_type_): _description_
    """
    __tablename__ = 'event_schedules_detail'
    rowid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    profile = Column(String)
    start_day_relative = Column(String)
    time = Column(String)
    schedule_name = Column(String)
    message_id = Column(String)
    reactions = Column(String)

    def create(self, session):
        session.add(self)
        session.commit()
