import pytest
from gbf.environment.environment_singleton import EnvironmentSingleton


class TestEnvironmentSingleton:

    @pytest.mark.asyncio
    async def test_singleton(self):
        s1 = EnvironmentSingleton()
        s2 = EnvironmentSingleton()
        assert s1 is s2

    @pytest.mark.asyncio
    async def test_environment_eval(self):

        env_singleton = EnvironmentSingleton()

        await env_singleton.clear()
        await env_singleton.set('TEST1', '1')
        await env_singleton.set('TEST2', '2')

        actual = await env_singleton.replace_env_eval('abc')
        assert actual == 'abc'

        actual = await env_singleton.replace_env_eval('ab${TEST1}c')
        assert actual == 'ab1c'

        actual = await env_singleton.replace_env_eval('ab${TEST1}cd${TEST1}e')
        assert actual == 'ab1cd1e'

        actual = await env_singleton.replace_env_eval('ab${TEST1}cd${TEST2}e')
        assert actual == 'ab1cd2e'
