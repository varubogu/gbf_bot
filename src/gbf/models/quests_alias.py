
from sqlalchemy import Column, Integer, String, select
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
    target_id = Column(Integer, primary_key=True)
    target_alias_id = Column(Integer, primary_key=True)
    alias = Column(String)
    alias_kana_small = Column(String)

    @classmethod
    async def select_all(
        cls,
        session,
    ) -> ['QuestsAlias']:
        result = await session.execute(
            select(cls)
        )
        return result.scalars().all()
