import pytest
import pytest_asyncio
from sqlalchemy import delete
from sqlalchemy.ext.asyncio.session import AsyncSession
from gbf.models.quests_alias import QuestsAlias


class TestQuestsAlias:

    @pytest_asyncio.fixture
    async def db_clear(self, async_db_session: AsyncSession):
        await async_db_session.execute(
            delete(QuestsAlias)
        )
        await async_db_session.commit()

    @pytest_asyncio.fixture(scope='function', autouse=True)
    async def test_data1(self) -> QuestsAlias:
        return QuestsAlias(
            target_id=1,
            target_alias_id=1,
            alias="tybh",
            alias_kana_small="つよばは"
        )

    @pytest_asyncio.fixture(scope='function', autouse=True)
    async def test_data2(self) -> QuestsAlias:
        return QuestsAlias(
            target_id=1,
            target_alias_id=2,
            alias="luci",
            alias_kana_small="つよばは"
        )

    @pytest_asyncio.fixture(scope='function', autouse=True)
    async def test_data3(self) -> QuestsAlias:
        return QuestsAlias(
            target_id=2,
            target_alias_id=1,
            alias="luci",
            alias_kana_small="ルシファーHard"
        )

    @pytest.mark.asyncio
    async def test_select_all(
        self,
        db_clear,
        async_db_session: AsyncSession,
        test_data1: QuestsAlias,
        test_data2: QuestsAlias,
        test_data3: QuestsAlias
    ):
        # データの作成
        async_db_session.add(test_data1)
        async_db_session.add(test_data2)
        async_db_session.add(test_data3)
        await async_db_session.commit()

        # select_all メソッドのテスト
        results = await QuestsAlias.select_all(
            async_db_session
        )
        assert len(results) == 3
        for r in results:

            if r.target_id == test_data1.target_id and \
                    r.target_alias_id == test_data1.target_alias_id:
                expect = test_data1
            elif r.target_id == test_data2.target_id and \
                    r.target_alias_id == test_data2.target_alias_id:
                expect = test_data2
            elif r.target_id == test_data3.target_id and \
                    r.target_alias_id == test_data3.target_alias_id:
                expect = test_data3
            else:
                assert False

            assert r.target_id == expect.target_id
            assert r.target_alias_id == expect.target_alias_id
            assert r.alias == expect.alias
            assert r.alias_kana_small == expect.alias_kana_small
