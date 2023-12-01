# FILEPATH: /workspaces/gbf_bot/tests/test_environments.py
import pytest
import pytest_asyncio
from sqlalchemy import delete
from sqlalchemy.ext.asyncio.session import AsyncSession
from gbf.models.guild_environments import GuildEnvironments


class TestGuildEnvironments:

    TEST_KEY_PREFIX = "TestGuildEnvironments"

    @pytest_asyncio.fixture
    async def db_clear(self, async_db_session: AsyncSession):
        await async_db_session.execute(
            delete(GuildEnvironments)
        )
        await async_db_session.commit()

    @pytest_asyncio.fixture(scope='function', autouse=True)
    async def data1(self) -> GuildEnvironments:
        return GuildEnvironments(
            guild_id=112233445566778899,
            key="TestGuildEnvironments1",
            value="0",
            memo=""
        )

    @pytest_asyncio.fixture(scope='function', autouse=True)
    async def data2_list(self) -> list[GuildEnvironments]:
        return [
            GuildEnvironments(
                guild_id=112233445566778899,
                key="TestGuildEnvironments2",
                value="1",
                memo=""
            ),
            GuildEnvironments(
                guild_id=112233445566778899,
                key="TestGuildEnvironments3",
                value="2",
                memo="aaa"
            ),
            GuildEnvironments(
                guild_id=999999999999999999,
                key="TestGuildEnvironments2",
                value="3",
                memo=""
            )
        ]

    @pytest.mark.asyncio
    async def test_select_single(
        self,
        db_clear,
        async_db_session: AsyncSession,
        data1: GuildEnvironments
    ):

        # テストデータの作成
        async_db_session.add(data1)
        await async_db_session.commit()

        result = await GuildEnvironments.select_single(
            async_db_session,
            data1.guild_id,
            data1.key
        )

        # 結果の検証
        assert result is not None
        assert result.guild_id == data1.guild_id
        assert result.key == data1.key
        assert result.value == data1.value
        assert result.memo == data1.memo

    @pytest.mark.asyncio
    async def test_select_multi(
        self,
        db_clear,
        async_db_session: AsyncSession,
        data1: GuildEnvironments,
        data2_list: list[GuildEnvironments]
    ):

        all_list = [data1] + data2_list

        # テストデータの作成
        for actual in all_list:
            async_db_session.add(actual)
        await async_db_session.commit()

        # 検証用データ抽出
        expected_list = [
            d for d in data2_list
            if d.guild_id == data2_list[1].guild_id and
            d.key in [data2_list[1].key, data2_list[2].key]
        ]

        # テスト対象のメソッドの呼び出し
        results = await GuildEnvironments.select_multi(
            async_db_session,
            data1.guild_id,
            [d.key for d in expected_list]
        )

        # 結果の検証
        assert results is not None
        assert len(results) == len(expected_list)
        for actual in results:
            expect = [
                d for d in expected_list
                if actual.key == d.key
            ][0]

            assert actual.guild_id == expect.guild_id
            assert actual.key == expect.key
            assert actual.value == expect.value
            assert actual.memo == expect.memo
        assert len([a for a in results if a.key == data1.key]) == 0

    @pytest.mark.asyncio
    async def test_select_all(
        self,
        db_clear,
        async_db_session: AsyncSession,
        data1: GuildEnvironments,
        data2_list: list[GuildEnvironments]
    ):
        # テストデータの作成

        expect_list = [data1] + data2_list

        for actual in expect_list:
            async_db_session.add(actual)
        await async_db_session.commit()

        # テスト対象のメソッドの呼び出し
        results = await GuildEnvironments.select_all(
            async_db_session,
            expect_list[0].guild_id
        )

        # 結果の検証
        expect_count = len(
            [d for d in expect_list if d.guild_id == expect_list[0].guild_id]
        )
        assert len(results) == expect_count
        for actual in results:
            expect = [
                d for d in expect_list
                if actual.key == d.key
            ][0]
            assert actual.key == expect.key
            assert actual.value == expect.value
            assert actual.memo == expect.memo

    @pytest.mark.asyncio
    async def test_delete_all(
        self,
        db_clear,
        async_db_session: AsyncSession,
        data2_list: list[GuildEnvironments]
    ):

        target_guild_id = data2_list[0].guild_id
        other_guild_id = data2_list[2].guild_id
        target_count = len(
            [d for d in data2_list if d.guild_id == target_guild_id]
        )

        # テストデータの作成
        for actual in data2_list:
            async_db_session.add(actual)
        await async_db_session.commit()

        results = await GuildEnvironments.select_all(
            async_db_session,
            target_guild_id
        )
        # テストデータ挿入を確認
        assert len(results) == target_count

        # テスト対象のメソッドの呼び出し
        await GuildEnvironments.delete_all(
            async_db_session,
            target_guild_id
        )

        # 対象サーバーのデータが削除されていることを確認
        results = await GuildEnvironments.select_all(
            async_db_session,
            target_guild_id
        )
        assert len(results) == 0

        # 他のサーバーのデータは削除されていないことを確認
        results = await GuildEnvironments.select_all(
            async_db_session,
            other_guild_id
        )
        assert len(results) >= 0
