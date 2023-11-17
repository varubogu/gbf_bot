
from datetime import datetime, timedelta
import uuid
from sqlalchemy \
    import UUID, Column, DateTime, BigInteger, Integer, UniqueConstraint, and_
from sqlalchemy.future import select
from gbf.models.model_base import ModelBase
from gbf.models.table_types import TableType
from gbf.models.table_scopes import TableScopes


def default_expiry_date():
    """有効期限の初期値

    Returns:
        datetime.datetime: 有効期限の初期値
    """
    return datetime.now() + timedelta(days=1)


class BattleRecruitments(ModelBase):
    """マルチバトル募集情報

    Args:
        Base (_type_): _description_
    """
    __tablename__ = 'battle_recruitments'
    __tabletype__ = TableType.Transaction
    __tablescope__ = TableScopes.Community
    row_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
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

    async def create(self, session):

        await session.add(self)
        await session.commit()

    @classmethod
    async def select_single(
        cls,
        session,
        guild_id: int,
        channel_id: int,
        message_id: int
    ) -> 'BattleRecruitments':
        """マルチバトル募集情報を検索する
        Args:
            session (Session): DB接続
            guild_id (int): 検索対象のサーバーID
            channel_id (int): 検索対象のチャンネルID
            message_id (int): 検索対象のメッセージID

        Returns:
            _type_: _description_
        """
        result = await session.execute(
            select(cls).filter(
                and_(
                    cls.guild_id == guild_id,
                    cls.channel_id == channel_id,
                    cls.message_id == message_id
                )
            )
        )

        return result.scalars().first()
