
from datetime import datetime, timedelta
from typing import Sequence
from sqlalchemy import BigInteger, Column, String, and_, delete
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from gbf.models.model_base import ModelBase
from gbf.models.table_scopes import TableScopes
from gbf.models.table_types import TableType
from gbf.utils.exception.environment_notfound_exception \
    import EnvironmentNotFoundException


async def default_expiry_date():
    return datetime.now() + timedelta(days=1)


class GuildEnvironments(ModelBase):
    """サーバー毎の環境変数

    Args:
        Base (_type_): _description_
    """
    __tablename__ = 'guild_environments'
    __tabletype__ = TableType.Reference
    __tablescope__ = TableScopes.Guild
    __table_args__ = (
        {'comment': 'サーバー毎の環境変数'}
    )
    
    guild_id = Column(BigInteger, primary_key=True, comment="サーバーID")
    key = Column(String, primary_key=True, comment="環境変数のキー")
    value = Column(String, comment="環境変数の値")
    memo = Column(String, comment="メモ")


    @classmethod
    async def select_single(
        cls,
        session: AsyncSession,
        guild_id: int,
        key: str
    ) -> 'GuildEnvironments':
        """
        環境変数を取得する
        Args:
            session (Session): DB接続
            guild_id (int): サーバー（Guild）ID
            key (str): 環境変数キー
        Returns:
            Environment: 環境変数オブジェクト
        Raises:
            EnvironmentNotFound: 環境変数が存在しない場合に発生する例外
        """
        result = await session.execute(
            select(cls).filter(and_(
                cls.key == key,
                cls.guild_id == guild_id
            ))
        )
        environment = result.scalars().first()
        if environment is None:
            raise EnvironmentNotFoundException(key)
        return environment

    @classmethod
    async def select_multi(
        cls,
        session: AsyncSession,
        guild_id: int,
        keys: str
    ) -> Sequence['GuildEnvironments']:
        """
        環境変数を一括取得する
        Args:
            session (Session): DB接続
            guild_id (int): サーバー（Guild）ID
            keys ([str]): 環境変数キーのリスト
        Returns:
            [Environment]: 環境変数オブジェクトのリスト

        """
        result = await session.execute(
            select(cls).filter(and_(
                cls.key.in_(keys),
                cls.guild_id == guild_id
            ))
        )
        return result.scalars().all()

    @classmethod
    async def select_all(
        cls,
        session: AsyncSession,
        guild_id: int
    ) -> Sequence['GuildEnvironments']:
        """
        環境変数を一括取得する
        Args:
            session (Session): DB接続
            guild_id (int): サーバー（Guild）ID
        Returns:
            [Environment]: 環境変数オブジェクトのリスト

        """
        result = await session.execute(
            select(cls).filter(cls.guild_id == guild_id)
        )
        return result.scalars().all()

    @classmethod
    async def delete_all(
        cls,
        session: AsyncSession,
        guild_id: int
    ) -> None:
        """
        環境変数を全て削除する

        """
        await session.execute(
            delete(cls).where(cls.guild_id == guild_id)
        )
        await session.commit()
