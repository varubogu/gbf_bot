from datetime import datetime

from gbf.models.event_schedule_details import EventScheduleDetails
from gbf.models.event_schedules import EventSchedules
from gbf.models.guild_channels import GuildChannels
from gbf.models.guild_event_schedule_details import GuildEventScheduleDetails
from gbf.models.schedules import Schedules
from gbf.schedules.calculator import ScheduleCalculator


class ScheduleManager:
    """
    スケジュール管理クラス
    """

    async def event_schedule_clear(self, session):
        """スケジュールを全て削除する

        Args:
            session (Session): DB接続
        """
        await Schedules.truncate(session)

    async def event_schedule_create(self, session):
        """スケジュール生成

        Args:
            session (Session): DB接続
        """

        # 必要なデータを全取得
        schedules = await EventSchedules.select_all(session)
        details = await EventScheduleDetails.select_all(session)
        guild_details = await GuildEventScheduleDetails.select_all(session)
        notifications = await GuildChannels.select_where_channel_type(
            session, 3
        )

        registration_schedules = await self.calc_schedule(
            schedules,
            details,
            guild_details,
            notifications
        )

        await Schedules.bulk_insert(session, registration_schedules)

    async def calc_schedule(
            self,
            all_schedules: list[EventSchedules],
            all_details: list[EventScheduleDetails],
            all_guild_details: list[GuildEventScheduleDetails],
            notification_channels: list[GuildChannels]
    ) -> list[Schedules]:
        """スケジュール計算

        Args:
            all_schedules (EventSchedules]): スケジュール一覧
            all_details (EventSchedulesDetails]): スケジュール詳細
            all_guild_details (GuildEventSchedulesDetails]): サーバー毎のスケジュール詳細
            notification_channels (_type_): スケジュール詳細で使うサーバーの通知先チャンネル
        """

        results: list[Schedules] = []

        for schedule in all_schedules:

            # 全サーバー共通のスケジュール詳細
            details = await self.filter_details(
                schedule,
                all_details
            )
            common_details_result = await self.common_details(
                schedule,
                details,
                notification_channels
            )
            results.extend(common_details_result)

            # サーバー毎のスケジュール詳細
            guild_details = await self.filter_guild_details(
                schedule,
                all_guild_details
            )
            common_details_result = await self.guild_details(
                schedule,
                guild_details
            )
            results.extend(common_details_result)

        return results

    async def filter_details(
            self,
            schedule: EventSchedules,
            details: list[EventScheduleDetails]
    ):
        return [d for d in details if d.profile == schedule.profile]

    async def filter_guild_details(
            self,
            schedule: EventSchedules,
            details: list[GuildEventScheduleDetails]
    ):
        return [d for d in details if d.profile == schedule.profile]

    async def common_details(
            self,
            schedule,
            details,
            notification_channels
    ) -> list[Schedules]:
        """_summary_

        Args:
            schedule (_type_): スケジュール
            details (_type_): スケジュール詳細
            notification_channels (_type_): 通知先チャンネル一覧

        Returns:
            [Schedules]: イベントスケジュールに紐づくギルド毎のスケジュール詳細リスト
        """
        results = []

        # 全サーバー共通のスケジュール詳細
        for detail in details:
            calculator = ScheduleCalculator(schedule, detail=detail)
            times = await calculator.calculate_times()

            for time in times:
                for notification_channel in notification_channels:
                    regist_schedule = await self.create_common_schedule(
                        schedule,
                        detail,
                        time,
                        notification_channel
                    )
                    results.append(regist_schedule)
        return results

    async def guild_details(
            self,
            schedule: EventSchedules,
            guild_details: GuildEventScheduleDetails
    ) -> list[Schedules]:
        """イベントスケジュールに紐づくギルド毎のスケジュール詳細を作成する

        Args:
            schedule (EventSchedules): スケジュール
            guild_details (GuildEventSchedulesDetails): サーバー毎のスケジュール詳細

        Returns:
            [Schedules]: イベントスケジュールに紐づくギルド毎のスケジュール詳細リスト
        """

        results = []

        for detail in guild_details:
            calculator = ScheduleCalculator(schedule, guild_detail=detail)
            times = await calculator.calculate_times()
            for time in times:
                regist_schedule = await self.create_guild_schedule(
                    schedule,
                    detail,
                    time
                )
                results.append(regist_schedule)
        return results

    async def create_common_schedule(
            self,
            schedule: EventSchedules,
            detail: EventScheduleDetails,
            time: datetime,
            notify_channel: GuildChannels
    ):
        """_summary_

        Args:
            schedule (EventSchedules): スケジュール
            detail (EventSchedulesDetails): スケジュール詳細
            time (datetime): スケジュール日時
            notify_channel (GuildChannels): 通知先チャンネル情報

        Returns:
            Schedules: スケジュール
        """
        s = Schedules()
        s.parent_schedule_id = schedule.row_id
        s.parent_schedule_detail_id = detail.row_id
        s.schedule_datetime = time
        s.guild_id = notify_channel.guild_id
        s.channel_id = notify_channel.channel_id
        s.message_id = detail.message_id
        return s

    async def create_guild_schedule(
            self,
            schedule: EventSchedules,
            detail: GuildEventScheduleDetails,
            time: datetime
    ):
        """サーバーのスケジュールを作成する

        Args:
            schedule (EventSchedules): スケジュール
            detail (GuildEventSchedulesDetails): サーバーのスケジュール詳細
            time (datetime): スケジュール日時
        Returns:
            Schedules: スケジュール
        """
        s = Schedules()
        s.parent_schedule_id = schedule.row_id
        s.parent_schedule_detail_id = detail.row_id
        s.schedule_datetime = time
        s.guild_id = detail.guild_id
        s.channel_id = detail.channel_id
        s.message_id = detail.message_id
        return s
