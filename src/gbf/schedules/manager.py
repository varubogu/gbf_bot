from datetime import datetime
from typing import Sequence
from gbf.enums.channel_type import ChannelType
from gbf.models.event_schedule_details import EventScheduleDetails
from gbf.models.event_schedules import EventSchedules
from gbf.models.guild_channels import GuildChannels
from gbf.models.guild_event_schedule_details import GuildEventScheduleDetails
from gbf.models.guild_event_schedules import GuildEventSchedules
from gbf.models.schedules import Schedules
from gbf.schedules.calculator import ScheduleCalculator
from sqlalchemy.ext.asyncio import AsyncSession


class ScheduleManager:
    """
    スケジュール管理クラス
    """

    async def event_schedule_clear(self, session: AsyncSession):
        """スケジュールを全て削除する

        Args:
            session (Session): DB接続
        """
        await Schedules.truncate(session)

    async def event_schedule_create(self, session: AsyncSession):
        """スケジュール生成

        Args:
            session (Session): DB接続
        """

        # 必要なデータを全取得
        global_schedules = await EventSchedules.select_all(session)
        global_details = await EventScheduleDetails.select_all(session)
        guild_schedules = await GuildEventSchedules.select_global_all(session)
        guild_details = await GuildEventScheduleDetails.select_global_all(session)
        guild_notifications = await GuildChannels.select_global_where_channel_type(
            session,
            ChannelType.NOTIFICATION.value
        )

        registration_schedules = await self.calc_schedule(
            global_schedules,
            global_details,
            guild_schedules,
            guild_details,
            guild_notifications
        )

        await Schedules.bulk_insert(session, registration_schedules)

    async def calc_schedule(
            self,
            global_schedules_all: Sequence[EventSchedules],
            global_details_all: Sequence[EventScheduleDetails],
            guild_schedules_all: Sequence[GuildEventSchedules],
            guild_details_all: Sequence[GuildEventScheduleDetails],
            notification_channels: Sequence[GuildChannels]
    ) -> list[Schedules]:
        """スケジュール計算

        Args:
            all_schedules (EventSchedules]): スケジュール一覧
            all_details (EventSchedulesDetails]): スケジュール詳細
            all_guild_details (GuildEventSchedulesDetails]): サーバー毎のスケジュール詳細
            notification_channels (_type_): スケジュール詳細で使うサーバーの通知先チャンネル
        """

        results: list[Schedules] = []

        # 全サーバー共通イベント
        for schedule in global_schedules_all:

            # globalイベント＋globalイベント詳細計算
            details = await self.filter_details(
                schedule,
                global_details_all
            )
            global_details_result = await self.global_calc(
                schedule,
                details,
                notification_channels
            )

            results.extend(global_details_result)

            # globalイベント＋guildイベント詳細計算
            guild_details = await self.filter_details(
                schedule,
                guild_details_all
            )
            global_details_result = await self.guild_calc(
                schedule,
                guild_details
            )
            results.extend(global_details_result)

        for guild_schedule in guild_schedules_all:
            # guildイベント＋guildイベント詳細計算
            guild_details_all = await self.filter_details(
                guild_schedule,
                guild_details_all
            )
            global_details_result = await self.guild_calc(
                guild_schedule,
                guild_details_all
            )
            results.extend(global_details_result)


        return results

    async def filter_details(
            self,
            schedule: EventSchedules | GuildEventSchedules,
            details: Sequence[EventScheduleDetails | GuildEventScheduleDetails]
    ) -> Sequence[EventScheduleDetails]:
        return [d for d in details if d.profile == schedule.profile]


    async def global_calc(
            self,
            schedule: EventSchedules,
            details: Sequence[EventScheduleDetails],
            notification_channels: Sequence[GuildChannels]
    ) -> list[Schedules]:
        """_summary_

        Args:
            schedule (_type_): スケジュール
            details (_type_): スケジュール詳細
            notification_channels (_type_): 通知先チャンネル一覧

        Returns:
            list[Schedules]: イベントスケジュールに紐づくギルド毎のスケジュール詳細リスト
        """
        results: list[Schedules] = []

        for detail in details:
            calculator = ScheduleCalculator(schedule, detail=detail)
            times = await calculator.calculate_times()

            for time in times:
                for notification_channel in notification_channels:
                    regist_schedule = await self.create_global_schedule(
                        schedule,
                        detail,
                        time,
                        notification_channel
                    )
                    results.append(regist_schedule)
        return results

    async def guild_calc(
            self,
            schedule: EventSchedules,
            guild_details: Sequence[GuildEventScheduleDetails]
    ) -> list[Schedules]:
        """イベントスケジュールに紐づくギルド毎のスケジュール詳細を作成する

        Args:
            schedule (EventSchedules): スケジュール
            guild_details (GuildEventSchedulesDetails): サーバー毎のスケジュール詳細

        Returns:
            list[Schedules]: イベントスケジュールに紐づくギルド毎のスケジュール詳細リスト
        """

        results: list[Schedules] = []

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

    async def create_global_schedule(
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
            schedule: EventSchedules | GuildEventSchedules,
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
