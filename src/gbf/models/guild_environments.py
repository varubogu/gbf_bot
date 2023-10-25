
from datetime import datetime, timedelta
from sqlalchemy import BigInteger, Column, String, and_, text
from sqlalchemy.future import select
from gbf.models.model_base import ModelBase
from gbf.models.table_types import TableType
from gbf.utils.exception.environment_notfound_exception \
    import EnvironmentNotFoundException


async def default_expiry_date():
    return datetime.now() + timedelta(days=1)


class GuildEnvironments(ModelBase):
    """環境変数

    Args:
        Base (_type_): _description_
    """
    __tablename__ = 'guild_environments'
    __tabletype__ = TableType.Reference
    guild_id = Column(BigInteger, primary_key=True)
    key = Column(String, primary_key=True)
    value = Column(String)
    memo = Column(String)

    @classmethod
    async def select_one(
        cls,
        session,
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
        environment = result.first()
        if environment is None:
            raise EnvironmentNotFoundException(key)
        return environment

    @classmethod
    async def select_multi(
        cls,
        session,
        guild_id: int,
        keys: str
    ) -> ['GuildEnvironments']:
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
    async def select_all(cls, session, guild_id: int) -> ['GuildEnvironments']:
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
    async def truncate(cls, session, guild_id: int) -> None:
        """
        環境変数を全て削除する

        """
        await session.execute(text(f'TRUNCATE {cls.__tablename__}'))
        await session.commit()
