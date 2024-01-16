import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio.session import AsyncSession
from gbf.models.guild_messages import GuildMessages


class TestGuildMessages:

    @pytest_asyncio.fixture(scope='function', autouse=True)
    async def test_data1(self) -> GuildMessages:
        return GuildMessages(
            guild_id=1111111111,
            message_id="111111111111",
            message_jp="日本語のテストメッセージ",
            reactions=":hai:",
            memo="テストメッセージ"
        )

    @pytest_asyncio.fixture(scope='function', autouse=True)
    async def test_data2(self) -> GuildMessages:
        return GuildMessages(
            guild_id=1111111111,
            message_id="2222222222",
            message_jp="日本語のテストメッセージ",
            reactions=":hai:",
            memo="テストメッセージ"
        )

    @pytest_asyncio.fixture(scope='function', autouse=True)
    async def test_data3_other_guild(self) -> GuildMessages:
        return GuildMessages(
            guild_id=222222222222,
            message_id="2222222222",
            message_jp="日本語のテストメッセージ",
            reactions=":hai:",
            memo="テストメッセージ"
        )

    @pytest.mark.asyncio
    async def test_select_single(
        self,
        async_db_session: AsyncSession,
        test_data1: GuildMessages
    ):

        async_db_session.add(test_data1)
        await async_db_session.commit()
        await async_db_session.refresh(test_data1)

        # テスト対象のメソッドの呼び出し
        result = await test_data1.select_single(
            async_db_session,
            test_data1.guild_id,
            test_data1.message_id
        )

        assert result is not None
        assert result.guild_id == test_data1.guild_id
        assert result.message_id == test_data1.message_id
        assert result.message_jp == test_data1.message_jp
        assert result.reactions == test_data1.reactions
        assert result.memo == test_data1.memo

        await async_db_session.rollback()

    @pytest.mark.asyncio
    async def test_select_all(
        self,
        async_db_session: AsyncSession,
        test_data1: GuildMessages,
        test_data2: GuildMessages,
        test_data3_other_guild: GuildMessages
    ):
        # テスト対象サーバーID
        target_guild_id = test_data1.guild_id
        # データの作成
        async_db_session.add(test_data1)
        async_db_session.add(test_data2)
        async_db_session.add(test_data3_other_guild)
        await async_db_session.commit()
        await async_db_session.refresh(test_data1)
        await async_db_session.refresh(test_data2)
        await async_db_session.refresh(test_data3_other_guild)

        # select_all メソッドのテスト
        results = await GuildMessages.select_multi(
            async_db_session,
            target_guild_id,
            [test_data1.message_id, test_data2.message_id]
        )
        assert len(results) == 2
        for r in results:

            if r.guild_id == target_guild_id and \
                    r.message_id == test_data1.message_id:
                expect = test_data1
            elif r.guild_id == target_guild_id and \
                    r.message_id == test_data2.message_id:
                expect = test_data2
            else:
                assert False

            assert r.guild_id == expect.guild_id
            assert r.message_id == expect.message_id
            assert r.message_jp == expect.message_jp
            assert r.reactions == expect.reactions
            assert r.memo == expect.memo
        await async_db_session.rollback()
