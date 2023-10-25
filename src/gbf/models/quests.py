
from sqlalchemy import Column, Integer
from gbf.models.model_base import ModelBase
from sqlalchemy import String

from gbf.models.table_types import TableType


class Quests(ModelBase):
    """クエスト情報

    Args:
        Base (_type_): _description_
    """
    __tablename__ = 'quests'
    __tabletype__ = TableType.Reference
    target_id = Column(Integer, primary_key=True)
    recruit_count = Column(Integer)
    quest_name = Column(String)
    quest_alias = Column(String)
    command = Column(String)
    use_battle_type = Column(String)
