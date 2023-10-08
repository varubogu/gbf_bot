from sqlalchemy import Column, String
from models.model_base import ModelBase


class Messages(ModelBase):
    """メッセージ定義

    Args:
        Base (_type_): _description_
    """
    __tablename__ = 'messages'
    message_id = Column(String, primary_key=True)
    message_jp = Column(String)
    reactions = Column(String)
    memo = Column(String)

    @classmethod
    def select(cls, session, message_id: str) -> 'Messages':
        return session.query(cls).filter(cls.message_id == message_id).first()
