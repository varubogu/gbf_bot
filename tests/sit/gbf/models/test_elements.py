import pytest
import pytest_asyncio

from sqlalchemy import delete
from sqlalchemy.ext.asyncio.session import AsyncSession

from gbf.models.elements import Elements


class TestElements:

    TEST_ELEMENT_ID = 99

    @pytest_asyncio.fixture
    async def db_clear(self, async_db_session: AsyncSession):
        await async_db_session.execute(
            delete(Elements).where(
                Elements.element_id == self.TEST_ELEMENT_ID
            )
        )
        await async_db_session.commit()

    @pytest_asyncio.fixture(scope='function', autouse=True)
    async def test_data1(self) -> Elements:
        return Elements(
            element_id=self.TEST_ELEMENT_ID,
            stamp="🔴",
            name_jp="火",
            name_en="Fire"
        )

    @pytest.mark.asyncio
    async def test_select(
        self,
        db_clear,
        async_db_session: AsyncSession,
        test_data1: Elements
    ):

        # テストデータの作成
        async_db_session.add(test_data1)
        await async_db_session.commit()

        # 結果の検証
        result = await Elements.select(
            async_db_session,
            test_data1.element_id
        )
        assert result is not None
        assert result.element_id == test_data1.element_id
        assert result.stamp == test_data1.stamp
        assert result.name_jp == test_data1.name_jp
        assert result.name_en == test_data1.name_en
