
from sqlalchemy import Column, Integer, BigInteger
from sqlalchemy.future import select
from gbf.models.model_base import ModelBase
from gbf.models.table_types import TableType


class GuildChannels(ModelBase):
    """サーバーチャンネル

    Args:
        Base (_type_): _description_
    """
    __tablename__ = 'guild_channels'
    __tabletype__ = TableType.Reference
    guild_id = Column(BigInteger, primary_key=True)
    channel_id = Column(BigInteger, primary_key=True)
    channel_type = Column(Integer)

    @classmethod
    async def select_where_channel_type(
        cls,
        session,
        channel_type: int
    ):
        result = await session.execute(
            select(cls).filter(
                GuildChannels.channel_type == channel_type
            )
        )
        return result.scalars().all()
