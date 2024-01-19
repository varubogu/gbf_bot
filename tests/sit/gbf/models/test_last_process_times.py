
from datetime import datetime
import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio.session import AsyncSession
from gbf.enums.last_process_type import LastProcessType
from gbf.models.last_process_times import LastProcessTimes


class TestLastProcessTimes:

    @pytest_asyncio.fixture
    async def test_data1(self) -> LastProcessTimes:
        return LastProcessTimes(
            process_type=LastProcessType.SCHEDULE.value,
            execute_time=datetime(2024, 2, 1, 23, 59, 59),
            memo="最終スケジュール実行日時"
        )

    @pytest.mark.asyncio
    async def test_select_single(
        self,
        test_data1: LastProcessTimes,
        async_db_session: AsyncSession
    ):
        async_db_session.add(test_data1)
        await async_db_session.commit()
        await async_db_session.refresh(test_data1)

        result = await LastProcessTimes.select_single(
            async_db_session,
            LastProcessType(test_data1.process_type)
        )
        assert result.process_type == test_data1.process_type

        await async_db_session.rollback()

    @pytest.mark.asyncio
    async def test_select_and_update(
        self,
        test_data1: LastProcessTimes,
        async_db_session: AsyncSession
    ):
        # refreshで前の値が消えてしまうため退避
        except_time = test_data1.execute_time

        async_db_session.add(test_data1)
        await async_db_session.commit()
        await async_db_session.refresh(test_data1)

        now = datetime.now()
        result = await LastProcessTimes.select_and_update(
            async_db_session,
            LastProcessType(test_data1.process_type),
        )
        # 5秒以内で合格
        assert abs((result[0] - except_time).total_seconds()) < 5
        assert abs((result[1] - now).total_seconds()) < 5
        await async_db_session.rollback()

    @pytest.mark.asyncio
    async def test_select_or_create(
        self,
        async_db_session: AsyncSession
    ):
        # Test select_or_create method
        process_type = LastProcessType.SCHEDULE
        result = await LastProcessTimes.select_or_create(
            async_db_session,
            process_type
        )
        assert result.process_type == process_type.value

        await async_db_session.rollback()

    @pytest.mark.asyncio
    async def test_create(
        self,
        async_db_session: AsyncSession
    ):
        # Test create method
        process_type = LastProcessType.SCHEDULE
        result = await LastProcessTimes.create(
            async_db_session,
            process_type
        )
        assert result.process_type == process_type.value

        await async_db_session.rollback()

    @pytest.mark.asyncio
    async def test_make(self):
        # Test make method
        process_type = LastProcessType.SCHEDULE
        result = await LastProcessTimes.make(process_type)
        assert result.process_type == process_type.value
