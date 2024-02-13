import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio.session import AsyncSession
from gbf.environment.environment_singleton import EnvironmentSingleton
from gbf.models.environments import Environments


class TestSitEnvironmentSingleton:

    @pytest_asyncio.fixture
    async def env_singleton(self):
        return EnvironmentSingleton()

    @pytest.mark.asyncio
    async def test_load_db(
            self,
            env_singleton: EnvironmentSingleton,
            async_db_session: AsyncSession
    ):
        try:
            await Environments.truncate(async_db_session)
            async_db_session.add(Environments(key='TEST1', value='1'))
            async_db_session.add(Environments(key='TEST2', value='2'))
            await async_db_session.commit()
            await env_singleton.load_db(async_db_session)

            actual = await env_singleton.replace_env_eval('abc')
            assert actual == 'abc'

            actual = await env_singleton.replace_env_eval('ab${TEST1}c')
            assert actual == 'ab1c'

            actual = await env_singleton.replace_env_eval('ab${TEST1}cd${TEST1}e')
            assert actual == 'ab1cd1e'

            actual = await env_singleton.replace_env_eval('ab${TEST1}cd${TEST2}e')
            assert actual == 'ab1cd2e'
        finally:
            await async_db_session.rollback()
