from datetime import datetime
import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio.session import AsyncSession
from gbf.models.schedules import Schedules


class TestSchedules:

    @pytest_asyncio.fixture(scope='function', autouse=True)
    async def test_data1(self) -> Schedules:
        return Schedules(
            row_id="bda6f178-881e-4a53-a921-51458b0c3cc3",
            parent_schedule_id="90002313-5971-42d4-be73-e395004005d1",
            parent_schedule_detail_id="50742b8e-033d-4529-ba2f-09e6965c228b",
            schedule_datetime=datetime(2021, 1, 1, 19, 0, 0),
            guild_id=111111,
            channel_id=222222,
            message_id="333333"
        )

    @pytest_asyncio.fixture(scope='function', autouse=True)
    async def test_data2(self) -> Schedules:
        return Schedules(
            row_id="e4cf54e0-fdcc-4690-aec4-3b2cba1c7af3",
            parent_schedule_id="90002313-5971-42d4-be73-e395004005d1",
            parent_schedule_detail_id="50742b8e-033d-4529-ba2f-09e6965c228b",
            schedule_datetime=datetime(2021, 1, 1, 19, 0, 1),
            guild_id=111111,
            channel_id=222222,
            message_id="333333"
        )

    @pytest_asyncio.fixture(scope='function', autouse=True)
    async def test_data3(self) -> Schedules:
        return Schedules(
            row_id="f2a259ab-33d3-479e-b4ea-ccd010fcba2b",
            parent_schedule_id="90002313-5971-42d4-be73-e395004005d1",
            parent_schedule_detail_id="50742b8e-033d-4529-ba2f-09e6965c228b",
            schedule_datetime=datetime(2021, 1, 1, 19, 0, 59),
            guild_id=111111,
            channel_id=222222,
            message_id="333333"
        )

    @pytest_asyncio.fixture(scope='function', autouse=True)
    async def test_data4(self) -> Schedules:
        return Schedules(
            row_id="cd39035f-a2d9-4ca0-9ffd-56a82fbdf4bb",
            parent_schedule_id="90002313-5971-42d4-be73-e395004005d1",
            parent_schedule_detail_id="50742b8e-033d-4529-ba2f-09e6965c228b",
            schedule_datetime=datetime(2021, 1, 1, 19, 1, 0),
            guild_id=111111,
            channel_id=222222,
            message_id="333333"
        )

    @pytest.mark.asyncio
    async def test_select_all(
        self,
        async_db_session: AsyncSession,
        test_data1: Schedules,
        test_data2: Schedules,
        test_data3: Schedules
    ):
        try:
            # データの作成
            async_db_session.add(test_data1)
            async_db_session.add(test_data2)
            async_db_session.add(test_data3)
            await async_db_session.commit()
            await async_db_session.refresh(test_data1)
            await async_db_session.refresh(test_data2)
            await async_db_session.refresh(test_data3)

            # select_all メソッドのテスト
            results = await Schedules.select_all(
                async_db_session
            )
            assert len(results) == 3
            for r in results:

                row_id = r.row_id

                if row_id == test_data1.row_id:
                    expect = test_data1
                elif row_id == test_data2.row_id:
                    expect = test_data2
                elif row_id == test_data3.row_id:
                    expect = test_data3
                else:
                    assert False

                assert row_id == expect.row_id
                assert r.parent_schedule_id == expect.parent_schedule_id
                assert r.parent_schedule_detail_id == expect.parent_schedule_detail_id
                assert r.schedule_datetime == expect.schedule_datetime
                assert r.guild_id == expect.guild_id
                assert r.channel_id == expect.channel_id
                assert r.message_id == expect.message_id
        finally:
            await async_db_session.rollback()

    @pytest.mark.asyncio
    async def test_bulk_insert(
            self,
            async_db_session: AsyncSession,
            test_data1,
            test_data2
    ):
        try:
            await Schedules.bulk_insert(async_db_session, [test_data1, test_data2])
            await async_db_session.commit()
            await async_db_session.refresh(test_data1)
            await async_db_session.refresh(test_data2)

            result = await Schedules.select_all(async_db_session)
            assert len(result) == 2
        finally:
            await async_db_session.rollback()

    @pytest.mark.asyncio
    async def test_truncate(
            self,
            async_db_session: AsyncSession,
            test_data1
    ):
        try:
            async_db_session.add(test_data1)
            await async_db_session.commit()
            await async_db_session.refresh(test_data1)

            await Schedules.truncate(async_db_session)

            result = await Schedules.select_all(async_db_session)
            assert len(result) == 0
        finally:
            await async_db_session.rollback()

    @pytest.mark.asyncio
    async def test_select_sinse_last_time(
            self,
            async_db_session: AsyncSession,
            test_data1,
            test_data2,
            test_data3,
            test_data4
    ):
        try:
            await Schedules.bulk_insert(
                async_db_session,
                [test_data1, test_data2, test_data3, test_data4]
            )
            await async_db_session.commit()
            await async_db_session.refresh(test_data1)
            await async_db_session.refresh(test_data2)
            await async_db_session.refresh(test_data3)
            await async_db_session.refresh(test_data4)

            last_time = datetime(2021, 1, 1, 19, 0, 0)
            now = datetime(2021, 1, 1, 19, 0, 59)

            result = await Schedules.select_sinse_last_time(
                async_db_session, last_time, now
            )
            assert len(result) == 2
            result[0].schedule_datetime == test_data2.schedule_datetime
            result[1].schedule_datetime == test_data3.schedule_datetime
        finally:
            await async_db_session.rollback()
