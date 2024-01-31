from datetime import datetime
from typing import Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from gbf.enums.last_process_type import LastProcessType
from gbf.models.last_process_times import LastProcessTimes
from gbf.models.schedules import Schedules


class MinuteScheduleExecutor:
    async def fetch_schedules(
            self,
            session: AsyncSession,
            now: datetime
    ) -> Sequence[Schedules]:
        (last, _now) = await LastProcessTimes.select_and_update(
            session,
            LastProcessType.SCHEDULE,
            now
        )
        await session.commit()

        return await Schedules.select_sinse_last_time(session, last, _now)
