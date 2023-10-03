
from sqlalchemy import Column, Integer
from models.base import Base
from sqlalchemy import String


class BattleType(Base):
    """マルチ募集種類

    Args:
        Base (_type_): _description_
    """
    __tablename__ = 'battle_type'
    type_id = Column(Integer, primary_key=True)
    name = Column(String)
    reactions = Column(String)
