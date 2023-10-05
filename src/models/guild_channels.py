
from sqlalchemy import Column, Integer, BigInteger
from models.base import Base


class GuildChannels(Base):
    """サーバーチャンネル

    Args:
        Base (_type_): _description_
    """
    __tablename__ = 'guild_channels'
    guild_id = Column(BigInteger, primary_key=True)
    channel_id = Column(BigInteger, primary_key=True)
    channel_type = Column(Integer)
