import pytest
import pytest_asyncio
from datetime import datetime, timedelta
from sqlalchemy.future import select
from sqlalchemy import delete
from sqlalchemy.ext.asyncio.session import AsyncSession
from gbf.models.event_schedules import EventSchedules


class TestEventSchedules:

    @pytest_asyncio.fixture
    async def db_clear(self, async_db_session: AsyncSession):
        await async_db_session.execute(
            delete(EventSchedules)
        )
        await async_db_session.commit()

    @pytest_asyncio.fixture(scope='function', autouse=True)
    async def test_data1(self) -> EventSchedules:
        now = datetime.now()
        return EventSchedules(
            row_id="d86404c9-5dba-415f-8b4c-53ecd38c6d94",
            event_type="古戦場",
            event_count=99999999,
            profile="古戦場通常",
            weak_attribute=0,
            start_at=now,
            end_at=now + timedelta(days=7)

        )

    @pytest_asyncio.fixture(scope='function', autouse=True)
    async def test_data2(self) -> EventSchedules:
        now = datetime.now()
        return EventSchedules(
            row_id="0497f749-1362-4955-b354-44dea52fae91",
            event_type="ドレバラ",
            event_count=99999999,
            profile="ドレバラ通常",
            weak_attribute=0,
            start_at=now,
            end_at=now + timedelta(days=7)
        )

    @pytest.mark.asyncio
    async def test_create(
        self,
        db_clear,
        async_db_session: AsyncSession,
        test_data1: EventSchedules
    ):

        # テスト対象のメソッドの呼び出し
        await test_data1.create(async_db_session)

        # 結果の検証
        result_data = await async_db_session.execute(
            select(EventSchedules).filter(
                EventSchedules.row_id == test_data1.row_id
            )
        )

        result = result_data.scalars().first()

        assert result is not None
        assert str(result.row_id) == test_data1.row_id
        assert result.event_type == test_data1.event_type
        assert result.event_count == test_data1.event_count
        assert result.profile == test_data1.profile
        assert result.weak_attribute == test_data1.weak_attribute
        assert result.start_at == test_data1.start_at
        assert result.end_at == test_data1.end_at

    @pytest.mark.asyncio
    async def test_select_all(
        self,
        db_clear,
        async_db_session: AsyncSession,
        test_data1: EventSchedules,
        test_data2: EventSchedules
    ):
        # データの作成
        async_db_session.add(test_data1)
        async_db_session.add(test_data2)
        await async_db_session.commit()

        # select_all メソッドのテスト
        results = await EventSchedules.select_all(async_db_session)
        assert len(results) == 2
        for r in results:

            row_id_str = str(r.row_id)

            if row_id_str == test_data1.row_id:
                expect = test_data1
            elif row_id_str == test_data2.row_id:
                expect = test_data2
            else:
                assert False

            assert row_id_str == expect.row_id
            assert r.event_type == expect.event_type
            assert r.event_count == expect.event_count
            assert r.profile == expect.profile
            assert r.weak_attribute == expect.weak_attribute
            assert r.start_at == expect.start_at
            assert r.end_at == expect.end_at
