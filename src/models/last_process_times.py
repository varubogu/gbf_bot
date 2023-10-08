from datetime import datetime, timedelta
from enums.last_process_type import LastProcessType
from sqlalchemy import Column, DateTime, Integer, String

from models.model_base import ModelBase


class LastProcessTimes(ModelBase):
    """最終実行日時

    Args:
        Base (_type_): _description_
    """
    __tablename__ = 'last_process_times'

    process_type = Column(Integer, primary_key=True)
    execute_time = Column(DateTime, nullable=True)
    memo = Column(String)

    @classmethod
    def select_one(
            cls,
            session,
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

        return session.query(LastProcessTimes).filter(
                LastProcessTimes.process_type == process_type.value
            ).first()

    @classmethod
    def select_and_update(
            cls,
            session,
            process_type: LastProcessType,
            now: datetime = None
    ) -> (datetime, datetime):
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

        last_process_time = cls.select_or_create(session, process_type)
        last = last_process_time.execute_time
        last_process_time.execute_time = now
        return (last, now)

    @classmethod
    def select_or_create(
        cls,
        session,
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

        last = cls.select_one(session, process_type)

        if last is None:
            last = cls.create(session, process_type)
        return last

    @classmethod
    def create(
            cls, session, process_type: LastProcessType
    ) -> 'LastProcessTimes':

        """データを新規登録する

        Args:
            session (_type_): DB接続
            process_type (LastProcessType): 実行種類

        Returns:
            LastProcessTime: LastProcessTimeオブジェクト
        """
        last = cls.make(process_type)
        session.add(last)

        return last

    @classmethod
    def make(cls, process_type: LastProcessType) -> 'LastProcessTimes':

        """データを作成する

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

        elif process_type == LastProcessType.SPREDSHEET_SYNC:
            last = LastProcessTimes()
            last.process_type = process_type.value
            last.execute_time = None
            last.memo = "最終Googleスプレッドシート同期日時"

        else:
            raise Exception("Invalid process type")

        return last
