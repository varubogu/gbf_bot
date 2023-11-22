from datetime import datetime, timedelta
from sqlalchemy import BigInteger, Column, DateTime, Integer, String, and_
from sqlalchemy.future import select

from gbf.enums.last_process_type import LastProcessType
from gbf.models.model_base import ModelBase
from gbf.models.table_scopes import TableScopes
from gbf.models.table_types import TableType


class GuildLastProcessTimes(ModelBase):
    """(guild)最終実行日時

    Args:
        Base (_type_): _description_
    """
    __tablename__ = 'guild_last_process_times'
    __tabletype__ = TableType.History
    __tablescope__ = TableScopes.Guild

    guild_id = Column(BigInteger, primary_key=True)
    process_type = Column(Integer, primary_key=True)
    execute_time = Column(DateTime, nullable=True)
    memo = Column(String)

    @classmethod
    async def select_single(
            cls,
            session,
            guild_id: int,
            process_type: LastProcessType
    ) -> 'GuildLastProcessTimes':
        """
        最終実行日時を取得する
        Args:
            session (Session): DB接続
            guild_id (int): サーバーID
            process_type (LastProcessType): 実行種類

        Returns:
            last: 最終実行日時
        """

        result = session.execute(
            select(GuildLastProcessTimes).filter(
                and_(
                    GuildLastProcessTimes.guild_id == guild_id,
                    GuildLastProcessTimes.process_type == process_type.value
                )
            )
        )

        return result.scalars().first()

    @classmethod
    async def select_and_update(
            cls,
            session,
            guild_id: int,
            process_type: LastProcessType,
            now: datetime = None
    ) -> (datetime, datetime):
        """最終日時を取得し、現在日時に更新する

        Args:
            session (Session): DB接続
            guild_id (int): サーバーID
            process_type (LastProcessType): 実行種類
            now (datetime, optional):
                現在日時、省略時は内部で現在日時を生成する. Defaults to None.

        Returns:
            last_process: 最終実行日時
            now: 現在日時
        """
        if now is None:
            now = datetime.now()

        last_process_time = await cls.select_or_create(
            session, guild_id, process_type)

        last = last_process_time.execute_time
        last_process_time.execute_time = now
        return (last, now)

    @classmethod
    async def select_or_create(
            cls,
            session,
            guild_id: int,
            process_type: LastProcessType
    ) -> 'GuildLastProcessTimes':
        """データを検索して返す
        存在しない場合は作成して返す

        Args:
            session (_type_): DB接続
            guild_id (int): サーバーID
            process_type (LastProcessType): 実行種類

        Returns:
            LastProcessTime: LastProcessTimeオブジェクト
        """

        last = await cls.select_single(session, guild_id, process_type)

        if last is None:
            last = await cls.create(session, guild_id, process_type)
        return last

    @classmethod
    async def create(
            cls,
            session,
            guild_id: int,
            process_type: LastProcessType
    ) -> 'GuildLastProcessTimes':

        """データを新規登録する

        Args:
            session (_type_): DB接続
            guild_id (int): サーバーID
            process_type (LastProcessType): 実行種類

        Returns:
            LastProcessTime: LastProcessTimeオブジェクト
        """
        last = await cls.make(guild_id, process_type)
        await session.add(last)

        return last

    @classmethod
    async def make(
            cls,
            guild_id: int,
            process_type: LastProcessType
    ) -> 'GuildLastProcessTimes':

        """データを作成する

        Args:
            guild_id (int): サーバーID
            process_type (LastProcessType): 実行種類

        Returns:
            LastProcessTime: LastProcessTimeオブジェクト
        """

        if process_type == LastProcessType.SCHEDULE:
            last = GuildLastProcessTimes()
            last.guild_id = guild_id
            last.process_type = process_type.value
            last.execute_time = datetime.now() - timedelta(minutes=1)
            last.memo = "最終スケジュール実行日時"

        elif process_type == LastProcessType.SPREDSHEET_LOAD:
            last = GuildLastProcessTimes()
            last.guild_id = guild_id
            last.process_type = process_type.value
            last.execute_time = None
            last.memo = "最終Googleスプレッドシート読み込み日時"

        elif process_type == LastProcessType.SPREDSHEET_PUSH:
            last = GuildLastProcessTimes()
            last.guild_id = guild_id
            last.process_type = process_type.value
            last.execute_time = None
            last.memo = "最終Googleスプレッドシート書き込み日時"

        else:
            raise Exception("Invalid process type")

        return last
