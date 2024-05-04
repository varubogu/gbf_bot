
import uuid
from sqlalchemy import UUID, BigInteger, Column, ForeignKey, text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.asyncio import AsyncSession
from gbf.models.model_base import ModelBase
from gbf.models.table_scopes import TableScopes
from gbf.models.table_types import TableType


class BattleRecruitmentSchedules(ModelBase):
    """スケジュール情報

    Args:
        Base (_type_): _description_
    """
    __tablename__ = 'battle_recruitment_schedules'
    __tabletype__ = TableType.Transaction
    __tablescope__ = TableScopes.All
    __table_args__ = (
        {'comment': 'マルチ募集スケジュール情報'}
    )
    
    row_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, comment="行ID")
    parent_id = Column(UUID(as_uuid=True), ForeignKey('schedules.row_id'), comment="スケジュール行ID")
    message_id = Column(BigInteger, comment="通知対象のマルチ募集メッセージのID")

    parent = relationship("Schedules", back_populates="children")


    async def insert(self, session: AsyncSession):
        session.add(self)

    async def delete(self, session: AsyncSession):
        await session.delete(self)

    @classmethod
    async def bulk_insert(
        cls,
        session: AsyncSession,
        schedules: list['BattleRecruitmentSchedules']
    ):
        """
        複数のスケジュール情報を一括で挿入する

        Args:
            session (Session): DB接続セッション
            schedules (list[BattleRecruitmentSchedules]): 挿入するスケジュール情報のリスト
        """
        session.add_all(schedules)

    @classmethod
    async def truncate(cls, session: AsyncSession):
        """
        テーブルのデータを全て削除する

        Args:
            session (Session): DB接続セッション
        """
        await session.execute(text(f'TRUNCATE {cls.__tablename__}'))
        await session.commit()

