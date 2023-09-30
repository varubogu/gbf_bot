
from datetime import datetime
import uuid
from sqlalchemy \
    import UUID, Column, DateTime, BigInteger, String, UniqueConstraint
from .base import Base, SessionLocal


class BattleRecruitment(Base):
    """バトル募集情報

    Args:
        Base (_type_): _description_
    """
    __tablename__ = 'battle_recruitment'
    rowid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    guild_id = Column(BigInteger, primary_key=True)
    channel_id = Column(BigInteger, primary_key=True)
    message_id = Column(BigInteger, primary_key=True)
    battle_id = Column(String)
    expiry_date = Column(DateTime, default=datetime.now)

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
