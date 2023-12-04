import pytest
import pytest_asyncio
from sqlalchemy import delete
from sqlalchemy.ext.asyncio.session import AsyncSession
from gbf.models.messages import Messages


class TestMessages:

    @pytest_asyncio.fixture
    async def db_clear(self, async_db_session: AsyncSession):
        await async_db_session.execute(
            delete(Messages)
        )
        await async_db_session.commit()

    @pytest_asyncio.fixture(scope='function', autouse=True)
    async def test_data1(self) -> Messages:
        return Messages(
            message_id="111111111111",
            message_jp="日本語のテストメッセージ",
            reactions=":hai:",
            memo="テストメッセージ"
        )

    @pytest_asyncio.fixture(scope='function', autouse=True)
    async def test_data2(self) -> Messages:
        return Messages(
            message_id="2222222222",
            message_jp="日本語のテストメッセージ",
            reactions=":hai:",
            memo="テストメッセージ"
        )

    @pytest_asyncio.fixture(scope='function', autouse=True)
    async def test_data3(self) -> Messages:
        return Messages(
            message_id="3333333333",
            message_jp="日本語のテストメッセージ",
            reactions=":hai:",
            memo="テストメッセージ"
        )

    @pytest.mark.asyncio
    async def test_select_single(
        self,
        db_clear,
        async_db_session: AsyncSession,
        test_data1: Messages
    ):

        async_db_session.add(test_data1)
        await async_db_session.commit()

        # テスト対象のメソッドの呼び出し
        result = await test_data1.select_single(
            async_db_session,
            test_data1.message_id
        )

        assert result is not None
        assert result.message_id == test_data1.message_id
        assert result.message_jp == test_data1.message_jp
        assert result.reactions == test_data1.reactions
        assert result.memo == test_data1.memo

    @pytest.mark.asyncio
    async def test_select_all(
        self,
        db_clear,
        async_db_session: AsyncSession,
        test_data1: Messages,
        test_data2: Messages,
        test_data3: Messages
    ):
        # データの作成
        async_db_session.add(test_data1)
        async_db_session.add(test_data2)
        async_db_session.add(test_data3)
        await async_db_session.commit()

        # select_all メソッドのテスト
        results = await Messages.select_multi(
            async_db_session,
            [test_data1.message_id, test_data2.message_id]
        )
        assert len(results) == 2
        for r in results:

            if r.message_id == test_data1.message_id:
                expect = test_data1
            elif r.message_id == test_data2.message_id:
                expect = test_data2
            else:
                assert False

            assert r.message_id == expect.message_id
            assert r.message_jp == expect.message_jp
            assert r.reactions == expect.reactions
            assert r.memo == expect.memo
