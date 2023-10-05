
from sqlalchemy import Column, Integer
from models.base import Base
from sqlalchemy import String


class ChannelTypes(Base):
    """チャンネル種類

    Args:
        Base (_type_): _description_
    """
    __tablename__ = 'channel_types'
    channel_type = Column(Integer, primary_key=True)
    channel_type_name = Column(String)
