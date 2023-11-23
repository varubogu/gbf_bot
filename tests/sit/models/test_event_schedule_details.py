import uuid
import pytest
import pytest_asyncio
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio.session import AsyncSession
from gbf.models.event_schedule_details import EventSchedulesDetails


class TestEventSchedulesDetails:

    @pytest_asyncio.fixture
    async def db_clear(self, async_db_session: AsyncSession):
        await async_db_session.execute(
            delete(EventSchedulesDetails)
        )
        await async_db_session.commit()

    @pytest_asyncio.fixture(scope='function', autouse=True)
    async def test_data1(self) -> EventSchedulesDetails:
        return EventSchedulesDetails(
            row_id="93dafb02-0e26-41ba-b909-26f560088517",
            profile="TestEventSchedulesDetails1",
            start_day_relative="0",
            time="00:00",
            schedule_name="TEST_SCHEDULE_NAME",
            message_id="TEST_MESSAGE_ID",
            guild_id=1234567890,
            channel_id=1234567890,
            reactions="☑️,❎",

        )

    @pytest_asyncio.fixture(scope='function', autouse=True)
    async def test_data2(self) -> EventSchedulesDetails:
        return EventSchedulesDetails(
            row_id="22560927-4566-4a3c-abbf-1e2de14bb147",
            profile="TestEventSchedulesDetails2",
            start_day_relative="0-7",
            time="23:59:59",
            schedule_name="TEST_SCHEDULE_NAME",
            message_id="TEST_MESSAGE_ID",
            guild_id=1234567890,
            channel_id=1234567890,
            reactions="☑️,❎",

        )

    @pytest.mark.asyncio
    async def test_create(
        self,
        db_clear,
        async_db_session: AsyncSession,
        test_data1: EventSchedulesDetails
    ):

        # テスト対象のメソッドの呼び出し
        await test_data1.create(async_db_session)

        # 結果の検証
        result_data = await async_db_session.execute(
            select(EventSchedulesDetails).filter(
                EventSchedulesDetails.row_id == test_data1.row_id
            )
        )

        result = result_data.scalars().first()

        assert result is not None
        assert str(result.row_id) == test_data1.row_id
        assert result.profile == test_data1.profile
        assert result.start_day_relative == test_data1.start_day_relative
        assert result.time == test_data1.time
        assert result.schedule_name == test_data1.schedule_name
        assert result.message_id == test_data1.message_id
        assert result.guild_id == test_data1.guild_id
        assert result.channel_id == test_data1.channel_id
        assert result.reactions == test_data1.reactions

    @pytest.mark.asyncio
    async def test_select_all(
        self,
        db_clear,
        async_db_session: AsyncSession,
        test_data1: EventSchedulesDetails,
        test_data2: EventSchedulesDetails
    ):
        # データの作成
        async_db_session.add(test_data1)
        async_db_session.add(test_data2)
        await async_db_session.commit()

        # select_all メソッドのテスト
        results = await EventSchedulesDetails.select_all(async_db_session)
        assert len(results) == 2
        for r in results:

            row_id_str = str(r.row_id)

            if row_id_str == test_data1.row_id:
                actual = test_data1
            elif row_id_str == test_data2.row_id:
                actual = test_data2
            else:
                assert False

            assert row_id_str == actual.row_id
            assert r.profile == actual.profile
            assert r.start_day_relative == actual.start_day_relative
            assert r.time == actual.time
            assert r.schedule_name == actual.schedule_name
            assert r.message_id == actual.message_id
            assert r.guild_id == actual.guild_id
            assert r.channel_id == actual.channel_id
            assert r.reactions == actual.reactions
