from sqlalchemy import Column, String, Integer
from models.model_base import ModelBase


class Elements(ModelBase):
    """属性定義

    Args:
        Base (_type_): _description_
    """
    __tablename__ = 'elements'
    element_id = Column(Integer, primary_key=True)
    stamp = Column
    name_jp = Column(String)
    name_en = Column(String)

    @classmethod
    def select(cls, session, element_id: int) -> 'Elements':
        return session.query(cls).filter(cls.element_id == element_id).first()
