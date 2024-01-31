from typing import Sequence
from sqlalchemy import Column, String
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from gbf.models.model_base import ModelBase
from gbf.models.table_scopes import TableScopes
from gbf.models.table_types import TableType


class Messages(ModelBase):
    """メッセージ定義

    Args:
        Base (_type_): _description_
    """
    __tablename__ = 'messages'
    __tabletype__ = TableType.Reference
    __tablescope__ = TableScopes.All
    message_id = Column(String, primary_key=True)
    message_jp = Column(String)
    reactions = Column(String)
    memo = Column(String)

    @classmethod
    async def select_single(
            cls,
            session: AsyncSession,
            message_id: str
    ) -> 'Messages':
        """
        単一のメッセージIDに基づいてメッセージを取得する

        Args:
            session (Session): DB接続セッション
            message_id (str): 選択するメッセージのID

        Returns:
            Messages: 指定されたメッセージIDに一致するメッセージオブジェクト
        """
        result = await session.execute(
            select(cls).filter(cls.message_id == message_id)
        )
        return result.scalars().first()

    @classmethod
    async def select_multi(
            cls,
            session: AsyncSession,
            message_ids: list[str]
    ) -> Sequence['Messages']:
        """
        複数のメッセージIDに基づいてメッセージを取得する

        Args:
            session (Session): DB接続セッション
            message_ids (list[str]): 選択するメッセージのIDのリスト

        Returns:
            list[Messages]: 指定されたメッセージIDに一致するメッセージオブジェクトのリスト
        """
        result = await session.execute(
            select(cls).filter(cls.message_id.in_(message_ids))
        )
        return result.scalars().all()
