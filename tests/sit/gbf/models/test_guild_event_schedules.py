import pytest
import pytest_asyncio
from datetime import datetime, timedelta
from sqlalchemy.future import select
from sqlalchemy import and_
from sqlalchemy.ext.asyncio.session import AsyncSession
from gbf.models.guild_event_schedules import GuildEventSchedules


class TestGuildEventSchedules:

    @pytest_asyncio.fixture(scope='function', autouse=True)
    async def test_data1(self) -> GuildEventSchedules:
        now = datetime.now()
        return GuildEventSchedules(
            row_id="d86404c9-5dba-415f-8b4c-53ecd38c6d94",
            guild_id=1234567890,
            event_type="古戦場",
            event_count=99999999,
            profile="古戦場通常",
            weak_attribute=0,
            start_at=now,
            end_at=now + timedelta(days=7)
        )

    @pytest_asyncio.fixture(scope='function', autouse=True)
    async def test_data2(self) -> GuildEventSchedules:
        now = datetime.now()
        return GuildEventSchedules(
            row_id="0497f749-1362-4955-b354-44dea52fae91",
            guild_id=1234567890,
            event_type="ドレバラ",
            event_count=99999999,
            profile="ドレバラ通常",
            weak_attribute=0,
            start_at=now,
            end_at=now + timedelta(days=7)
        )

    @pytest_asyncio.fixture(scope='function', autouse=True)
    async def test_data3(self) -> GuildEventSchedules:
        now = datetime.now()
        return GuildEventSchedules(
            row_id="36101e7a-a8cc-4183-9274-746c453b48cb",
            guild_id=1111111111,
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
        async_db_session: AsyncSession,
        test_data1: GuildEventSchedules
    ):

        # テスト対象のメソッドの呼び出し
        await test_data1.create(async_db_session)
        await async_db_session.refresh(test_data1)

        # 結果の検証
        result_data = await async_db_session.execute(
            select(GuildEventSchedules).filter(and_(
                GuildEventSchedules.row_id == test_data1.row_id,
                GuildEventSchedules.guild_id == test_data1.guild_id
            ))
        )

        result = result_data.scalars().first()

        assert result is not None
        assert result.row_id == test_data1.row_id
        assert result.guild_id == test_data1.guild_id
        assert result.event_type == test_data1.event_type
        assert result.event_count == test_data1.event_count
        assert result.profile == test_data1.profile
        assert result.weak_attribute == test_data1.weak_attribute
        assert result.start_at == test_data1.start_at
        assert result.end_at == test_data1.end_at

        await async_db_session.rollback()

    @pytest.mark.asyncio
    async def test_select_all(
        self,
        async_db_session: AsyncSession,
        test_data1: GuildEventSchedules,
        test_data2: GuildEventSchedules,
        test_data3: GuildEventSchedules
    ):
        # テスト対象サーバーID
        target_guild_id = test_data1.guild_id
        # データの作成
        async_db_session.add(test_data1)
        async_db_session.add(test_data2)
        async_db_session.add(test_data3)
        await async_db_session.commit()
        await async_db_session.refresh(test_data1)
        await async_db_session.refresh(test_data2)
        await async_db_session.refresh(test_data3)

        # select_all メソッドのテスト
        results = await GuildEventSchedules.select_all(
            async_db_session,
            target_guild_id
        )
        assert len(results) == 2
        for r in results:

            row_id_str = r.row_id

            if row_id_str == test_data1.row_id:
                expect = test_data1
            elif row_id_str == test_data2.row_id:
                expect = test_data2
            else:
                assert False

            assert row_id_str == expect.row_id
            assert r.guild_id == expect.guild_id
            assert r.event_type == expect.event_type
            assert r.event_count == expect.event_count
            assert r.profile == expect.profile
            assert r.weak_attribute == expect.weak_attribute
            assert r.start_at == expect.start_at
            assert r.end_at == expect.end_at
        await async_db_session.rollback()
