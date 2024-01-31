
from typing import Sequence
from sqlalchemy import Column, Integer, String, select
from sqlalchemy.ext.asyncio import AsyncSession
from gbf.models.model_base import ModelBase
from gbf.models.table_scopes import TableScopes

from gbf.models.table_types import TableType


class Quests(ModelBase):
    """クエスト情報

    Args:
        Base (_type_): _description_
    """
    __tablename__ = 'quests'
    __tabletype__ = TableType.Reference
    __tablescope__ = TableScopes.All
    target_id = Column(Integer, primary_key=True)
    recruit_count = Column(Integer)
    quest_name = Column(String)
    use_battle_type = Column(String)
    default_battle_type = Column(String)

    @classmethod
    async def select_single(
        cls,
        session: AsyncSession,
        target_id: int
    ) -> list['Quests']:
        """
        特定のクエスト情報を取得する

        Args:
            session (Session): DB接続セッション
            target_id (Integer): ターゲットID

        Returns:
            Quests: クエスト情報
        """
        result = await session.execute(
            select(cls).filter(Quests.target_id == target_id)
        )
        return result.scalars().first()


    @classmethod
    async def select_all(
        cls,
        session: AsyncSession
    ) -> Sequence['Quests']:
        """
        すべてのクエスト情報を取得する

        Args:
            session (Session): DB接続セッション

        Returns:
            list[Quests]: すべてのクエスト情報のリスト
        """
        result = await session.execute(
            select(cls)
        )
        return result.scalars().all()
