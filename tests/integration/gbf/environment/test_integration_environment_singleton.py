import pytest
from gbf.environment.environment_singleton import EnvironmentSingleton
from gbf.models.environments import Environments


class TestIntegrationEnvironmentSingleton:

    @pytest.fixture
    async def setup(self):
        pass

    @pytest.mark.asyncio
    async def test_environment_eval(self, async_db_session):
        env_singleton = EnvironmentSingleton()
        await env_singleton.clear()

        session = await anext(async_db_session)

        await Environments.truncate(session)
        session.add(Environments(key='TEST1', value='1'))
        session.add(Environments(key='TEST2', value='2'))
        await session.commit()
        await env_singleton.load_db(session)

        actual = await env_singleton.replace_env_eval('abc')
        assert actual == 'abc'

        actual = await env_singleton.replace_env_eval('ab${TEST1}c')
        assert actual == 'ab1c'

        actual = await env_singleton.replace_env_eval('ab${TEST1}cd${TEST1}e')
        assert actual == 'ab1cd1e'

        actual = await env_singleton.replace_env_eval('ab${TEST1}cd${TEST2}e')
        assert actual == 'ab1cd2e'
