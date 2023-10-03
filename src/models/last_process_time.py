from datetime import datetime, timedelta
from enums.last_process_type import LastProcessType
from sqlalchemy import Column, DateTime, Integer, String

from models.base import Base


class LastProcessTime(Base):
    """最終実行日時

    Args:
        Base (_type_): _description_
    """
    __tablename__ = 'last_process_time'

    process_type = Column(Integer, primary_key=True)
    execute_time = Column(DateTime, nullable=True)
    memo = Column(String)

    @classmethod
    def select(
            cls,
            session,
            process_type: LastProcessType
    ) -> 'LastProcessTime':
        """
        最終実行日時を取得する
        Args:
            session (Session): DB接続
            process_type (LastProcessType): 実行種類

        Returns:
            last: 最終実行日時
        """

        return session.query(LastProcessTime).filter(
                LastProcessTime.process_type == process_type.value
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
    ) -> 'LastProcessTime':
        """データを検索して返す
        存在しない場合は作成して返す

        Args:
            session (_type_): DB接続
            process_type (LastProcessType): 実行種類

        Returns:
            LastProcessTime: LastProcessTimeオブジェクト
        """

        last = cls.select(session, process_type)

        if last is None:
            last = cls.create(session, process_type)
        return last

    @classmethod
    def create(
            cls, session, process_type: LastProcessType
    ) -> 'LastProcessTime':

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
    def make(cls, process_type: LastProcessType) -> 'LastProcessTime':

        """データを作成する

        Args:
            process_type (LastProcessType): 実行種類

        Returns:
            LastProcessTime: LastProcessTimeオブジェクト
        """

        if process_type == LastProcessType.SCHEDULE:
            last = LastProcessTime()
            last.process_type = process_type.value
            last.execute_time = datetime.now() - timedelta(minutes=1)
            last.memo = "最終スケジュール実行日時"

        elif process_type == LastProcessType.SPREDSHEET_SYNC:
            last = LastProcessTime()
            last.process_type = process_type.value
            last.execute_time = None
            last.memo = "最終Googleスプレッドシート同期日時"

        else:
            raise Exception("Invalid process type")

        return last
