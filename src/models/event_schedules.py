import uuid
from sqlalchemy \
    import UUID, Column, UniqueConstraint, \
    DateTime, BigInteger, Integer, String
from models.base import Base


class EventSchedules(Base):
    """イベントスケジュール情報

    Args:
        Base (_type_): _description_
    """
    __tablename__ = 'event_schedules'
    rowid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
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
            name='unique_event'
        ),
    )

    def create(self, session):
        session.add(self)
        session.commit()
