
from sqlalchemy import Column, Integer
from models.base import Base
from sqlalchemy import String


class Quests(Base):
    """クエスト情報

    Args:
        Base (_type_): _description_
    """
    __tablename__ = 'quests'
    target_id = Column(Integer, primary_key=True)
    recruit_count = Column(Integer)
    quest_name = Column(String)
    quest_alias = Column(String)
    use_battle_type = Column(String)
