import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio.session import AsyncSession
from gbf.models.environments import Environments


class TestEnvironments:

    TEST_KEY_PREFIX = "TestEnvironments"

    @pytest_asyncio.fixture(scope='function', autouse=True)
    async def data1(self) -> Environments:
        return Environments(
            key="TestEnvironments1",
            value="0",
            memo=""
        )

    @pytest_asyncio.fixture(scope='function', autouse=True)
    async def data2_list(self) -> list[Environments]:
        return [
            Environments(
                key="TestEnvironments2",
                value="1",
                memo=""
            ),
            Environments(
                key="TestEnvironments3",
                value="2",
                memo="aaa"
            ),
            Environments(
                key="TestEnvironments4",
                value="3",
                memo=""
            )
        ]

    @pytest.mark.asyncio
    async def test_select_single(
        self,
        async_db_session: AsyncSession,
        data1: Environments
    ):

        # テストデータの作成
        async_db_session.add(data1)
        await async_db_session.commit()
        await async_db_session.refresh(data1)

        result = await Environments.select_single(
            async_db_session,
            data1.key
        )

        # 結果の検証
        assert result is not None
        assert result.key == data1.key
        assert result.value == data1.value
        assert result.memo == data1.memo

        await async_db_session.rollback()

    @pytest.mark.asyncio
    async def test_select_multi(
        self,
        async_db_session: AsyncSession,
        data1: Environments,
        data2_list: list[Environments]
    ):

        all_list = [data1] + data2_list

        # テストデータの作成
        for actual in all_list:
            async_db_session.add(actual)
        await async_db_session.commit()
        for actual in all_list:
            await async_db_session.refresh(actual)

        # テスト対象のメソッドの呼び出し
        results = await Environments.select_multi(
            async_db_session,
            [d.key for d in data2_list]
        )

        # 結果の検証
        assert results is not None
        assert len(results) == len(data2_list)
        for actual in results:
            expect = [
                expect_single for expect_single in data2_list
                if actual.key == expect_single.key
            ][0]
            assert actual.key == expect.key
            assert actual.value == expect.value
            assert actual.memo == expect.memo
        assert len([a for a in results if a.key == data1.key]) == 0

        await async_db_session.rollback()

    @pytest.mark.asyncio
    async def test_select_all(
        self,
        async_db_session: AsyncSession,
        data1: Environments,
        data2_list: list[Environments]
    ):
        # テストデータの作成

        all_list = [data1] + data2_list

        for actual in all_list:
            async_db_session.add(actual)
        await async_db_session.commit()
        for actual in all_list:
            await async_db_session.refresh(actual)

        # テスト対象のメソッドの呼び出し
        results = await Environments.select_all(
            async_db_session
        )

        # 結果の検証
        assert len(results) == len(all_list)
        for actual in results:
            expect = [
                expect_single for expect_single in all_list
                if actual.key == expect_single.key
            ][0]
            assert actual.key == expect.key
            assert actual.value == expect.value
            assert actual.memo == expect.memo

        await async_db_session.rollback()

    @pytest.mark.asyncio
    async def test_truncate(
        self,
        async_db_session: AsyncSession,
        data2_list: list[Environments]
    ):

        # テストデータの作成
        for actual in data2_list:
            async_db_session.add(actual)
        await async_db_session.commit()
        for actual in data2_list:
            await async_db_session.refresh(actual)

        results = await Environments.select_all(async_db_session)
        assert len(results) == len(data2_list)

        # テスト対象のメソッドの呼び出し
        await Environments.truncate(async_db_session)

        # 結果の検証
        results = await Environments.select_all(async_db_session)
        assert len(results) == 0

        await async_db_session.rollback()
