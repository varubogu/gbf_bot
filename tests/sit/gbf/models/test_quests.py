import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio.session import AsyncSession
from gbf.models.quests import Quests


class TestQuests:

    @pytest_asyncio.fixture(scope='function', autouse=True)
    async def test_data1(self) -> Quests:
        return Quests(
            target_id=1,
            recruit_count=18,
            quest_name="プロトバハムートHL",
            use_battle_type="0",
            default_battle_type="0"
        )

    @pytest_asyncio.fixture(scope='function', autouse=True)
    async def test_data2(self) -> Quests:
        return Quests(
            target_id=2,
            recruit_count=6,
            quest_name="ダークラプチャーHard",
            use_battle_type="0,1,2",
            default_battle_type="0"
        )

    @pytest_asyncio.fixture(scope='function', autouse=True)
    async def test_data3(self) -> Quests:
        return Quests(
            target_id=3,
            recruit_count=18,
            quest_name="プロトバハムートHL",
            use_battle_type="1",
            default_battle_type="1"
        )

    @pytest.mark.asyncio
    async def test_select_all(
        self,
        async_db_session: AsyncSession,
        test_data1: Quests,
        test_data2: Quests,
        test_data3: Quests
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
            results = await Quests.select_all(
                async_db_session
            )
            assert len(results) == 3
            for r in results:

                if r.target_id == test_data1.target_id and \
                        r.target_id == test_data1.target_id:
                    expect = test_data1
                elif r.target_id == test_data2.target_id and \
                        r.target_id == test_data2.target_id:
                    expect = test_data2
                elif r.target_id == test_data3.target_id and \
                        r.target_id == test_data3.target_id:
                    expect = test_data3
                else:
                    assert False

                assert r.target_id == expect.target_id
                assert r.recruit_count == expect.recruit_count
                assert r.quest_name == expect.quest_name
                assert r.use_battle_type == expect.use_battle_type
                assert r.default_battle_type == expect.default_battle_type
        finally:
            await async_db_session.rollback()

