
from datetime import datetime, timedelta
import uuid
from sqlalchemy \
    import UUID, Column, DateTime, BigInteger, Integer, UniqueConstraint
from models.base import Base, SessionLocal


def default_expiry_date():
    return datetime.now() + timedelta(days=1)


class BattleRecruitment(Base):
    """バトル募集情報

    Args:
        Base (_type_): _description_
    """
    __tablename__ = 'battle_recruitment'
    rowid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    guild_id = Column(BigInteger)
    channel_id = Column(BigInteger)
    message_id = Column(BigInteger)
    target_id = Column(Integer)
    battle_type_id = Column(Integer)
    expiry_date = Column(DateTime, default=default_expiry_date)

    __table_args__ = (
        UniqueConstraint(
            'guild_id',
            'channel_id',
            'message_id',
            name='unique_message'
        ),
    )

    def create(self):
        try:
            SessionLocal.add(self)
            SessionLocal.commit()
        except Exception as e:
            print(e)

    @classmethod
    def read(cls, message_id: int) -> 'BattleRecruitment':
        SessionLocal.get(cls)
