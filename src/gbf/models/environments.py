
from datetime import datetime, timedelta
from sqlalchemy import Column, String, text
from sqlalchemy.future import select
from gbf.models.model_base import ModelBase
from gbf.models.table_scopes import TableScopes
from gbf.models.table_types import TableType
from gbf.utils.exception.environment_notfound_exception \
    import EnvironmentNotFoundException


async def default_expiry_date():
    return datetime.now() + timedelta(days=1)


class Environments(ModelBase):
    """環境変数

    Args:
        Base (_type_): _description_
    """
    __tablename__ = 'environments'
    __tabletype__ = TableType.Reference
    __tablescope__ = TableScopes.All
    key = Column(String, primary_key=True)
    value = Column(String)
    memo = Column(String)

    @classmethod
    async def select_single(cls, session, key: str) -> 'Environments':
        """
        環境変数を取得する
        Args:
            session (Session): DB接続
            key (str): 環境変数キー
        Returns:
            Environment: 環境変数オブジェクト
        Raises:
            EnvironmentNotFound: 環境変数が存在しない場合に発生する例外
        """
        result = await session.execute(
            select(cls).filter(cls.key == key)
        )
        environment = result.scalars().first()
        if environment is None:
            raise EnvironmentNotFoundException(key)
        return environment

    @classmethod
    async def select_multi(cls, session, keys: [str]) -> ['Environments']:
        """
        環境変数を一括取得する

        """
        result = await session.execute(
            select(cls).filter(cls.key.in_(keys))
        )
        return result.scalars().all()

    @classmethod
    async def select_all(cls, session) -> ['Environments']:
        """
        環境変数を一括取得する

        """
        result = await session.execute(
            select(cls)
        )
        return result.scalars().all()

    @classmethod
    async def truncate(cls, session) -> None:
        """
        環境変数を全て削除する

        """
        await session.execute(text(f'TRUNCATE {cls.__tablename__}'))
        await session.commit()
