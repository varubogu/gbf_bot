from datetime import datetime
from typing import Sequence
import uuid
from sqlalchemy import UUID, BigInteger, Column, DateTime, String, and_, text
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship, selectinload
from gbf.models.battle_recruitment_schedules import BattleRecruitmentSchedules
from gbf.models.model_base import ModelBase
from gbf.models.table_scopes import TableScopes
from gbf.models.table_types import TableType


class Schedules(ModelBase):
    """スケジュール情報

    Args:
        Base (_type_): _description_
    """
    __tablename__ = 'schedules'
    __tabletype__ = TableType.Transaction
    __tablescope__ = TableScopes.All
    __table_args__ = (
        {'comment': 'スケジュール情報'}
    )
    
    row_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, comment="行ID")
    parent_schedule_id = Column(
        UUID(as_uuid=True), nullable=True, default=None, comment="作成元のイベントスケジュールテーブルの行ID")
    parent_schedule_detail_id = Column(
        UUID(as_uuid=True), nullable=True, default=None, comment="作成元のイベント期間内詳細スケジュールテーブルの行ID")
    schedule_datetime = Column(DateTime, comment="スケジュール日時")
    guild_id = Column(BigInteger, comment="サーバーID")
    channel_id = Column(BigInteger, comment="チャンネルID")
    message_id = Column(String, comment="メッセージテーブルのメッセージID")

    children = relationship("BattleRecruitmentSchedules", back_populates="parent")


    async def insert(self, session: AsyncSession):
        session.add(self)

    async def delete(self, session: AsyncSession):
        await session.delete(self)

    @classmethod
    async def bulk_insert(
        cls,
        session: AsyncSession,
        schedules: list['Schedules']
    ):
        """
        複数のスケジュール情報を一括で挿入する

        Args:
            session (Session): DB接続セッション
            schedules (list[Schedules]): 挿入するスケジュール情報のリスト
        """
        session.add_all(schedules)

    @classmethod
    async def truncate(cls, session: AsyncSession):
        """
        テーブルのデータを全て削除する

        Args:
            session (Session): DB接続セッション
        """
        await session.execute(text(f'TRUNCATE {cls.__tablename__}, {BattleRecruitmentSchedules.__tablename__}'))
        await session.commit()

    @classmethod
    async def select_sinse_last_time(
            cls,
            session: AsyncSession,
            last_time: datetime,
            now: datetime
    ) -> Sequence['Schedules']:
        """
        指定された日時の以降のスケジュール情報を取得する

        Args:
            session (Session): DB接続セッション
            last_time (datetime): 指定された日時
            now (datetime): 現在の日時
        
        Returns:
            list['Schedules']: 指定された日時以降のスケジュール情報のリスト
        """
        result = await session.execute(
            select(Schedules).filter(
                and_(
                    last_time < Schedules.schedule_datetime,
                    Schedules.schedule_datetime <= now
                )
            ).options(selectinload(Schedules.children))
        )
        return result.scalars().all()

    @classmethod
    async def select_all(
        cls,
        session: AsyncSession
    ) -> Sequence['Schedules']:
        """
        全てのスケジュール情報を取得する

        Args:
            session (Session): DB接続セッション
        
        Returns:
            list['Schedules']: 全てのスケジュール情報のリスト
        """
        result = await session.execute(
            select(Schedules)
        )
        return result.scalars().all()
