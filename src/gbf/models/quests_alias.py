
from typing import Sequence
from sqlalchemy import Column, Integer, String, UniqueConstraint, select
from sqlalchemy.ext.asyncio import AsyncSession
from gbf.models.model_base import ModelBase
from gbf.models.table_scopes import TableScopes

from gbf.models.table_types import TableType


class QuestsAlias(ModelBase):
    """クエスト別名情報

    Args:
        Base (_type_): _description_
    """
    __tablename__ = 'quests_alias'
    __tabletype__ = TableType.Reference
    __tablescope__ = TableScopes.All
    __table_args__ = (
        UniqueConstraint(
            'alias',
            name='unique_quests_alias'
        ),
        {'comment': 'クエスト別名情報'}
    )

    target_id = Column(Integer, primary_key=True, comment="クエストID")
    target_alias_id = Column(Integer, primary_key=True, comment="クエスト別名ID")
    alias = Column(String, comment="クエスト別名")
    alias_kana_small = Column(String, comment="クエスト別名半角カナ")


    @classmethod
    async def select_all(
        cls,
        session: AsyncSession,
    ) -> Sequence['QuestsAlias']:
        """
        すべてのクエスト別名情報を取得する

        Args:
            session (Session): DB接続セッション

        Returns:
            list[QuestsAlias]: すべてのクエスト別名情報のリスト
        """
        result = await session.execute(
            select(cls)
        )
        return result.scalars().all()
