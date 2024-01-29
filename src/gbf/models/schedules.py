from datetime import datetime
import uuid
from sqlalchemy import UUID, BigInteger, Column, DateTime, String, and_, text
from sqlalchemy.future import select
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
        session.add(self)

    async def delete(self, session):
        await session.delete(self)

    @classmethod
    async def bulk_insert(cls, session, schedules):
        """
        複数のスケジュール情報を一括で挿入する

        Args:
            session (Session): DB接続セッション
            schedules (list[Schedules]): 挿入するスケジュール情報のリスト
        """
        session.add_all(schedules)

    @classmethod
    async def truncate(cls, session):
        """
        テーブルのデータを全て削除する

        Args:
            session (Session): DB接続セッション
        """
        await session.execute(text('TRUNCATE schedules'))
        await session.commit()

    @classmethod
    async def select_sinse_last_time(
            cls,
            session,
            last_time: datetime,
            now: datetime
    ) -> list['Schedules']:
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
            )
        )
        return result.scalars().all()

    @classmethod
    async def select_all(cls, session) -> list['Schedules']:
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
