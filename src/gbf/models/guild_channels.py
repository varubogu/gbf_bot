
from typing import Sequence
from sqlalchemy import Column, Integer, BigInteger, and_
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from gbf.models.model_base import ModelBase
from gbf.models.table_scopes import TableScopes
from gbf.models.table_types import TableType


class GuildChannels(ModelBase):
    """サーバーチャンネル

    Args:
        Base (_type_): _description_
    """
    __tablename__ = 'guild_channels'
    __tabletype__ = TableType.Reference
    __tablescope__ = TableScopes.Guild
    guild_id = Column(BigInteger, primary_key=True)
    channel_id = Column(BigInteger, primary_key=True)
    channel_type = Column(Integer)

    @classmethod
    async def select_global_all(
        cls,
        session: AsyncSession
    ) -> Sequence['GuildChannels']:
        """
        ギルドチャンネルを全て取得します
        Args:
            session (Session): DB接続セッション
        Returns:
            list[GuildChannels]: チャンネルタイプに一致するギルドチャンネルのリスト
        """
        result = await session.execute(
            select(cls)
        )
        return result.scalars().all()


    @classmethod
    async def select_where_channel_type(
        cls,
        session: AsyncSession,
        guild_id: int,
        channel_type: int
    ) -> Sequence['GuildChannels']:
        """
        チャンネルタイプに基づいてギルドチャンネルを取得します
        Args:
            session (Session): DB接続セッション
            guild_id (int): サーバーID
            channel_type (int): チャンネルタイプ
        Returns:
            list[GuildChannels]: チャンネルタイプに一致するギルドチャンネルのリスト
        """
        result = await session.execute(
            select(cls).filter(and_(
                    GuildChannels.channel_type == channel_type,
                    GuildChannels.guild_id == guild_id
            ))
        )
        return result.scalars().all()

    @classmethod
    async def select_global_where_channel_type(
        cls,
        session: AsyncSession,
        channel_type: int
    ) -> Sequence['GuildChannels']:
        """
        チャンネルタイプに基づいてギルドチャンネルを取得します
        Args:
            session (Session): DB接続セッション
            channel_type (int): チャンネルタイプ
        Returns:
            list[GuildChannels]: チャンネルタイプに一致するギルドチャンネルのリスト
        """
        result = await session.execute(
            select(cls).filter(and_(
                    GuildChannels.channel_type == channel_type
            ))
        )
        return result.scalars().all()
