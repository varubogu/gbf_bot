
from sqlalchemy import Column, Integer
from gbf.models.model_base import ModelBase
from sqlalchemy import String

from gbf.models.table_types import TableType


class ChannelTypes(ModelBase):
    """チャンネル種類

    Args:
        Base (_type_): _description_
    """
    __tablename__ = 'channel_types'
    __tabletype__ = TableType.Reference
    channel_type = Column(Integer, primary_key=True)
    channel_type_name = Column(String)
    memo = Column(String)
