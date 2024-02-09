import uuid
from typing import Sequence

from sqlalchemy import UUID, BigInteger, Column, String
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from gbf.models.model_base import ModelBase
from gbf.models.table_scopes import TableScopes
from gbf.models.table_types import TableType


class GuildEventScheduleDetails(ModelBase):
    """サーバー毎のイベント期間内詳細スケジュール

    Args:
        Base (_type_): _description_
    """
    __tablename__ = 'guild_event_schedule_details'
    __tabletype__ = TableType.Reference
    __tablescope__ = TableScopes.Guild
    __table_args__ = (
        {'comment': 'サーバー毎のイベント期間内詳細スケジュール'}
    )
    
    row_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, comment="行ID")
    guild_id = Column(BigInteger, primary_key=True, comment="サーバーID")
    profile = Column(String, comment="(guild)イベントスケジュールとの紐づけプロファイル")
    start_day_relative = Column(String, comment="開始日からの相対日（数値または数値範囲）")
    time = Column(String, comment="イベントの時間 例：23:59")
    schedule_name = Column(String, comment="スケジュール名")
    message_id = Column(String, comment="メッセージテーブルのメッセージID")
    channel_id = Column(BigInteger, comment="チャンネルID")
    # TODO:チャンネルIDではなくチャンネル種類にすべき
    reactions = Column(String, comment="イベントメッセージに付与するリアクション")


    async def create(self, session: AsyncSession):
        session.add(self)
        await session.commit()

    @classmethod
    async def select_global_all(
        cls,
        session: AsyncSession
    ) -> Sequence['GuildEventScheduleDetails']:
        """
        ギルドイベントスケジュールの詳細を全て取得する
        Args:
            session (Session): DB接続セッション
        Returns:
            list[GuildEventScheduleDetails]: ギルドイベントスケジュール詳細のリスト
        """
        result = await session.execute(select(cls))
        return result.scalars().all()
