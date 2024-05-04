
from datetime import datetime, timedelta
from typing import Sequence
import uuid
from sqlalchemy \
    import UUID, Column, DateTime, BigInteger, Integer, \
    String, UniqueConstraint, and_
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
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
    __table_args__ = (
        UniqueConstraint(
            'guild_id',
            'channel_id',
            'message_id',
            name='unique_message'
        ),
        {'comment': 'マルチバトル募集情報'}
    )
    
    row_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, comment="行ID")
    guild_id = Column(BigInteger, comment="サーバーID")
    channel_id = Column(BigInteger, comment="チャンネルID")
    message_id = Column(BigInteger, comment="メッセージID")
    target_id = Column(Integer, comment="対象クエストID")
    battle_type_id = Column(Integer, comment="バトル種類ID")
    room_id = Column(String, comment="共闘部屋ID")
    expiry_date = Column(DateTime, default=default_expiry_date, comment="有効期限")
    recruit_end_message_id = Column(BigInteger, comment="募集終了メッセージID")


    async def create(self, session: AsyncSession):

        session.add(self)
        await session.commit()

    @classmethod
    async def select_single(
            cls,
            session: AsyncSession,
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

    @classmethod
    async def select_single_row_lock(
            cls,
            session: AsyncSession,
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
            ).with_for_update()
        )

        return result.scalars().first()

    @classmethod
    async def select_global_all(
            cls,
            session: AsyncSession,
    ) -> Sequence['BattleRecruitments']:
        """マルチバトル募集情報を一括取得する
        Args:
            session (Session): DB接続
            guild_id (int): 検索対象のサーバーID

        Returns:
            list[BattleRecruitments]: 一括取得結果
        """
        result = await session.execute(
            select(cls)
        )

        return result.scalars().all()
