import re
from datetime import datetime, timedelta
from models.event_schedules import EventSchedules
from models.event_schedule_details import EventSchedulesDetails
from models.guild_event_schedule_details import GuildEventSchedulesDetails
from util.convert_time import convert_time


class ScheduleCalculator():
    """スケジュール日時計算クラス
    """

    def __init__(
            self,
            schedule: EventSchedules,
            detail: EventSchedulesDetails = None,
            guild_detail: GuildEventSchedulesDetails = None,
    ):
        """スケジュール日時計算初期化
        計算に使う値を格納する

        Args:
            schedule (EventSchedules): スケジュール
            detail (EventSchedulesDetails): スケジュール詳細
            guild_detail (GuildEventSchedulesDetails): サーバー毎のスケジュール詳細
        """
        self.start_at: datetime = schedule.start_at
        self.end_at: datetime = schedule.end_at
        self.start_day_relative: str = None
        self.start_day_relative: str = None

        if detail:
            self.start_day_relative = detail.start_day_relative
            self.time = detail.time
        elif guild_detail:
            self.start_day_relative = guild_detail.start_day_relative
            self.time = guild_detail.time

    async def calculate_times(self) -> [datetime]:
        """日時を計算する

        Returns:
            [datetime]: スケジュール日時リスト
        """
        return await self._calculate_times(
            self.start_at,
            self.end_at,
            self.start_day_relative,
            self.time
        )

    async def _calculate_times(
            self,
            start_at: datetime,
            end_at: datetime,
            start_day_relative: str,
            time: str
    ) -> [datetime]:
        """条件に従ってスケジュール日時を計算する

        Args:
            start_at (datetime): スケジュール開始日
            end_at (datetime): スケジュール終了日
            start_day_relative (str): スケジュール開始日からの相対日
            time (str): スケジュール時間の文字列

        Raises:
            TypeError: start_day_relative is None
            Exception: time is None
            TypeError: start_day_relative is not matched

        Returns:
            [datetime]: スケジュール日時リスト
        """
        if start_day_relative is None:
            raise TypeError("start_day_relative is None")

        relative_day = start_day_relative.strip()

        if time is None:
            raise TypeError("start_day_relative is None")

        if relative_day == '*' or relative_day == 'all':
            # 全日実行
            return await self.all_date(start_at, end_at, time)

        if relative_day == 'start':
            # 開始日
            return await self.start_day(start_at, time)

        if relative_day == 'end':
            # 終了日
            return await self.end_day(end_at, time)

        range_match = re.compile(r'^(-?\d+)\s*(?:-|to)\s*(-?\d+)$')
        range_matched = range_match.match(relative_day)
        if range_matched:
            # 日付範囲
            return await self.range_day(start_at, time, range_matched)

        num_match = re.compile(r'^-?\d+$')
        num_matched = num_match.match(relative_day)
        if num_matched:
            # 日数（マイナスも可）
            return await self.num_day(start_at, start_day_relative, time)

        raise TypeError(f"start_relative_dayが不正です [{self.start_day_relative}]")

    async def all_date(
            self,
            start_at: datetime,
            end_at: datetime,
            time: str
    ) -> [datetime]:
        """全日程の日時を作成する

        Args:
            start_at (datetime): スケジュール開始日
            end_at (datetime): スケジュール終了日
            start_day_relative (str): スケジュール開始日からの相対日
            time (str): スケジュール時間の文字列

        Returns:
            [datetime]: スケジュール日時リスト
        """
        # 開始日の日時を生成
        start = convert_time(time, start_at)

        # イベント期間の日数を計算
        diff_days = (end_at - start_at).days
        deltas = [timedelta(days=i) for i in range(diff_days)]

        # 日付範囲から期間外を除く
        results = [
            start + delta
            for delta in deltas
            if start_at <= start + delta
            and start + delta <= end_at
        ]
        return results

    async def start_day(
            self,
            start_at: datetime,
            time: str
    ) -> [datetime]:
        """開始日を計算する

        Args:
            start_at (datetime): スケジュール開始日
            time (str): スケジュール時間の文字列

        Returns:
            [datetime]: スケジュール日時リスト
        """
        # 開始日
        return [convert_time(time, start_at)]

    async def end_day(
            self,
            end_at: datetime,
            time: str
    ) -> [datetime]:
        """終了日を計算する

        Args:
            end_at (datetime): スケジュール終了日
            time (str): スケジュール時間の文字列

        Returns:
            [datetime]: スケジュール日時リスト
        """
        # 開始日
        return [convert_time(time, end_at)]

    async def range_day(
            self,
            start_at: datetime,
            time: str,
            matched: re.Match[str]
    ) -> [datetime]:
        """開始日終了日の範囲を計算する

        Args:
            start_at (datetime): スケジュール開始日
            time (str): スケジュール時間の文字列
            matched (Match[str]): 範囲の正規表現マッチ結果

        Returns:
            [datetime]: スケジュール日時リスト
        """
        start_rel_day, end_rel_day = matched.groups()

        # 開始日時を生成
        start = convert_time(time, start_at)

        # イベント対象期間分の時間計算オブジェクトを生成
        results = [
            start + timedelta(days=i)
            for i in range(int(start_rel_day), int(end_rel_day) + 1)
        ]
        return results

    async def num_day(
            self,
            start_at: datetime,
            start_day_relative: str,
            time: str
    ) -> [datetime]:
        """該当日時を計算する

        Args:
            start_at (datetime): スケジュール開始日
            time (str): スケジュール時間の文字列
            matched (Match[str]): 範囲の正規表現マッチ結果

        Returns:
            [datetime]: スケジュール日時リスト
        """
        relative_day = start_day_relative.strip()

        start = convert_time(time, start_at)

        delta = timedelta(days=int(relative_day))

        return [start + delta]
