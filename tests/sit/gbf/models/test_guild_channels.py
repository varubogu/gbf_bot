import pytest
import pytest_asyncio
from sqlalchemy import delete
from gbf.models.guild_channels import GuildChannels
from sqlalchemy.ext.asyncio.session import AsyncSession


class TestGuildChannels:
    @pytest_asyncio.fixture
    async def db_clear(self, async_db_session: AsyncSession):
        await async_db_session.execute(
            delete(GuildChannels)
        )
        await async_db_session.commit()

    @pytest_asyncio.fixture(scope='function', autouse=True)
    async def test_data1(self) -> GuildChannels:
        return GuildChannels(
            guild_id=112233445566778899,
            channel_id=1111222233334444,
            channel_type=0
        )

    @pytest_asyncio.fixture(scope='function', autouse=True)
    async def test_data2(self) -> GuildChannels:
        return GuildChannels(
            guild_id=1234567890123456,
            channel_id=444455556666555,
            channel_type=9
        )

    @pytest.mark.asyncio
    async def test_select_where_channel_type(
        self,
        db_clear,
        async_db_session: AsyncSession,
        test_data1: GuildChannels,
        test_data2: GuildChannels,
    ):
        # データの作成
        async_db_session.add(test_data1)
        async_db_session.add(test_data2)
        await async_db_session.commit()

        # select_all メソッドのテスト
        results1 = await GuildChannels.select_where_channel_type(
            async_db_session,
            test_data1.channel_type
        )
        assert len(results1) == 1
        await self.equals_test_data(results1[0], test_data1)

        results2 = await GuildChannels.select_where_channel_type(
            async_db_session,
            test_data2.channel_type
        )
        assert len(results2) == 1
        await self.equals_test_data(results2[0], test_data2)

    async def equals_test_data(
            self,
            actual: GuildChannels,
            expected: GuildChannels
    ):
        assert actual.guild_id == expected.guild_id
        assert actual.channel_id == expected.channel_id
        assert actual.channel_type == expected.channel_type
