
from sqlalchemy import Column, Integer
from gbf.models.model_base import ModelBase
from sqlalchemy import String

from gbf.models.table_types import TableType


class BattleTypes(ModelBase):
    """マルチ募集種類

    Args:
        Base (_type_): _description_
    """
    __tablename__ = 'battle_types'
    __tabletype__ = TableType.Reference
    type_id = Column(Integer, primary_key=True)
    name = Column(String)
    reactions = Column(String)
