
from datetime import datetime, timedelta
from typing import Sequence
from sqlalchemy import Column, String, text
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
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
    __table_args__ = (
        {'comment': '環境変数'}
    )
    
    key = Column(String, primary_key=True, comment="環境変数のキー")
    value = Column(String, comment="環境変数の値")
    memo = Column(String, comment="メモ")


    @classmethod
    async def select_single(
        cls,
        session: AsyncSession,
        key: str
    ) -> 'Environments':
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
    async def select_multi(
        cls,
        session: AsyncSession,
        keys: list[str]
    ) -> Sequence['Environments']:
        """
        環境変数を一括取得する

        """
        result = await session.execute(
            select(cls).filter(cls.key.in_(keys))
        )
        return result.scalars().all()

    @classmethod
    async def select_all(cls, session: AsyncSession) -> Sequence['Environments']:
        """
        環境変数を一括取得する

        """
        result = await session.execute(
            select(cls)
        )
        return result.scalars().all()

    @classmethod
    async def truncate(cls, session: AsyncSession) -> None:
        """
        環境変数を全て削除する

        """
        await session.execute(text(f'TRUNCATE {cls.__tablename__}'))
        await session.commit()
