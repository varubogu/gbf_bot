from datetime import datetime, timedelta
from typing import Tuple

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from gbf.enums.last_process_type import LastProcessType
from gbf.models.model_base import ModelBase
from gbf.models.table_scopes import TableScopes
from gbf.models.table_types import TableType


class LastProcessTimes(ModelBase):
    """最終処理実行日時

    Args:
        Base (_type_): _description_
    """
    __tablename__ = 'last_process_times'
    __tabletype__ = TableType.History
    __tablescope__ = TableScopes.All
    __table_args__ = (
        {'comment': '最終処理実行日時'}
    )

    process_type = Column(Integer, primary_key=True, comment="処理種類")
    execute_time = Column(DateTime, nullable=True, comment="処理実行日時")
    memo = Column(String, comment="メモ")


    @classmethod
    async def select_single(
            cls,
            session: AsyncSession,
            process_type: LastProcessType
    ) -> 'LastProcessTimes':
        """
        最終実行日時を取得する
        Args:
            session (Session): DB接続
            process_type (LastProcessType): 実行種類

        Returns:
            last: 最終実行日時
        """

        result = await session.execute(
            select(LastProcessTimes).filter(
                LastProcessTimes.process_type == process_type.value
            )
        )
        return result.scalars().first()

    @classmethod
    async def select_and_update(
            cls,
            session: AsyncSession,
            process_type: LastProcessType,
            now: datetime | None = None
    ) -> Tuple[datetime, datetime]:
        """最終日時を取得し、現在日時に更新する

        Args:
            session (Session): DB接続
            process_type (LastProcessType): 実行種類
            now (datetime, optional):
                現在日時、省略時は内部で現在日時を生成する. Defaults to None.

        Returns:
            last_process: 最終実行日時
            now: 現在日時
        """
        if now is None:
            now = datetime.now()

        last_process_time = await cls.select_or_create(session, process_type)
        last = last_process_time.execute_time
        last_process_time.execute_time = now
        return (last, now)

    @classmethod
    async def select_or_create(
        cls,
        session: AsyncSession,
        process_type: LastProcessType
    ) -> 'LastProcessTimes':
        """データを検索して返す
        存在しない場合は作成して返す

        Args:
            session (_type_): DB接続
            process_type (LastProcessType): 実行種類

        Returns:
            LastProcessTime: LastProcessTimeオブジェクト
        """

        last = await cls.select_single(session, process_type)

        if last is None:
            last = await cls.create(session, process_type)
        return last

    @classmethod
    async def create(
            cls,
            session: AsyncSession,
            process_type: LastProcessType
    ) -> 'LastProcessTimes':

        """データを新規登録する

        Args:
            session (_type_): DB接続
            process_type (LastProcessType): 実行種類

        Returns:
            LastProcessTime: LastProcessTimeオブジェクト
        """
        last = await cls.make(process_type)
        session.add(last)

        return last

    @classmethod
    async def make(cls, process_type: LastProcessType) -> 'LastProcessTimes':

        """データを作成する（登録はしない）

        Args:
            process_type (LastProcessType): 実行種類

        Returns:
            LastProcessTime: LastProcessTimeオブジェクト
        """

        if process_type == LastProcessType.SCHEDULE:
            last = LastProcessTimes()
            last.process_type = process_type.value
            last.execute_time = datetime.now() - timedelta(minutes=1)
            last.memo = "最終スケジュール実行日時"

        elif process_type == LastProcessType.SPREADSHEET_LOAD:
            last = LastProcessTimes()
            last.process_type = process_type.value
            last.execute_time = None
            last.memo = "最終Googleスプレッドシート読み込み日時"

        elif process_type == LastProcessType.SPREADSHEET_PUSH:
            last = LastProcessTimes()
            last.process_type = process_type.value
            last.execute_time = None
            last.memo = "最終Googleスプレッドシート書き込み日時"

        else:
            raise Exception("Invalid process type")

        return last
