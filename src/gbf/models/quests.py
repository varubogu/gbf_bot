
from sqlalchemy import Column, Integer, select
from gbf.models.model_base import ModelBase
from sqlalchemy import String
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
        session,
        target_id
    ) -> ['Quests']:
        result = await session.execute(
            select(cls).filter(Quests.target_id == target_id)
        )
        return result.scalars().first()


    @classmethod
    async def select_all(
        cls,
        session
    ) -> ['Quests']:
        result = await session.execute(
            select(cls)
        )
        return result.scalars().all()
