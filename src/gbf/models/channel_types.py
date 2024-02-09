
from sqlalchemy import Column, Integer
from gbf.models.model_base import ModelBase
from sqlalchemy import String
from gbf.models.table_scopes import TableScopes

from gbf.models.table_types import TableType


class ChannelTypes(ModelBase):
    """チャンネル種類

    Args:
        Base (_type_): _description_
    """
    __tablename__ = 'channel_types'
    __tabletype__ = TableType.Reference
    __tablescope__ = TableScopes.All
    __table_args__ = (
        {'comment': 'チャンネル種類'}
    )

    channel_type = Column(Integer, primary_key=True, comment="チャンネル種類ID")
    channel_type_name = Column(String, comment="チャンネル種類名")
    memo = Column(String, comment="メモ")
