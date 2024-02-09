from typing import Sequence
import uuid
from sqlalchemy \
    import UUID, Column, UniqueConstraint, \
    DateTime, BigInteger, Integer, String
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from gbf.models.model_base import ModelBase
from gbf.models.table_scopes import TableScopes
from gbf.models.table_types import TableType


class EventSchedules(ModelBase):
    """イベントスケジュール

    Args:
        Base (_type_): _description_
    """
    __tablename__ = 'event_schedules'
    __tabletype__ = TableType.Reference
    __tablescope__ = TableScopes.All
    __table_args__ = (
        UniqueConstraint(
            'event_type',
            'event_count',
            name='unique_event'
        ),
        {'comment': 'イベントスケジュール'}
    )

    row_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, comment="行ID")
    event_type = Column(String, comment="イベント種類")
    event_count = Column(BigInteger, comment="イベント開催回数")
    profile = Column(String, comment="イベントスケジュール詳細との紐づけプロファイル")
    weak_attribute = Column(Integer, comment="有利属性")
    start_at = Column(DateTime, comment="開始日")
    end_at = Column(DateTime, comment="終了日")


    async def create(self, session: AsyncSession):
        """イベントスケジュールを作成する

        Args:
            session (Session): DB接続セッション

        Raises:
            SQLAlchemyError: DB操作でエラーが発生した場合に発生する例外
        """
        session.add(self)
        await session.commit()

    @classmethod
    async def select_all(
            cls,
            session: AsyncSession
    ) -> Sequence['EventSchedules']:
        """
        全てのイベントスケジュールを取得する
        Args:
            session (Session): DB接続セッション
        Returns:
            list[EventSchedules]: イベントスケジュールのリスト
        """
        result = await session.execute(select(cls))
        return result.scalars().all()
