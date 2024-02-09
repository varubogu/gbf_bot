
from sqlalchemy import Column, Integer
from gbf.models.model_base import ModelBase
from sqlalchemy import String
from gbf.models.table_scopes import TableScopes

from gbf.models.table_types import TableType


class BattleTypes(ModelBase):
    """マルチバトル戦術

    Args:
        Base (_type_): _description_
    """
    __tablename__ = 'battle_types'
    __tabletype__ = TableType.Reference
    __tablescope__ = TableScopes.All
    __table_args__ = (
        {'comment': 'マルチバトル戦術'}
    )

    type_id = Column(Integer, primary_key=True, comment="戦術ID")
    name = Column(String, comment="戦術名")
    reactions = Column(String, comment="戦術に応じたリアクション")
