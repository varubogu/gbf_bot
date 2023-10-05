
from sqlalchemy import Column, Integer
from models.base import Base
from sqlalchemy import String


class BattleTypes(Base):
    """マルチ募集種類

    Args:
        Base (_type_): _description_
    """
    __tablename__ = 'battle_types'
    type_id = Column(Integer, primary_key=True)
    name = Column(String)
    reactions = Column(String)
