import pytest
import pytest_asyncio
from gbf.environment.environment_singleton import EnvironmentSingleton


class TestUnitEnvironmentSingleton:

    @pytest_asyncio.fixture
    async def env_singleton(self) -> EnvironmentSingleton:
        env_singleton = EnvironmentSingleton()
        await env_singleton.clear()
        await env_singleton.set('TEST1', '1')
        await env_singleton.set('TEST2', '2')

        return env_singleton

    @pytest.mark.asyncio
    async def test_singleton(self):
        s1 = EnvironmentSingleton()
        s2 = EnvironmentSingleton()
        assert s1 is s2

    @pytest.mark.asyncio
    async def test_environment_eval(
            self,
            env_singleton: EnvironmentSingleton
    ):

        actual = await env_singleton.replace_env_eval('abc')
        assert actual == 'abc'

        actual = await env_singleton.replace_env_eval('ab${TEST1}c')
        assert actual == 'ab1c'

        actual = await env_singleton.replace_env_eval('ab${TEST1}cd${TEST1}e')
        assert actual == 'ab1cd1e'

        actual = await env_singleton.replace_env_eval('ab${TEST1}cd${TEST2}e')
        assert actual == 'ab1cd2e'

    @pytest.mark.asyncio
    async def test_find_env_keys_empty(
            self,
            env_singleton: EnvironmentSingleton
    ):
        a = 'abcdef'
        actual = await env_singleton.find_env_keys(a)
        assert len(actual) == 0

    @pytest.mark.asyncio
    async def test_find_env_keys_match(
            self,
            env_singleton: EnvironmentSingleton
    ):
        a = 'abc${TEST1}def'
        actual = await env_singleton.find_env_keys(a)
        assert len(actual) == 1

        a = 'abc${TEST1}de${TEST2}f'
        actual = await env_singleton.find_env_keys(a)
        assert len(actual) == 2

        # '$'が無い場合
        a = 'abc${TEST1}de{TEST2}f'
        actual = await env_singleton.find_env_keys(a)
        assert len(actual) == 1

    @pytest.mark.asyncio
    async def test_substr_env_key(
            self,
            env_singleton: EnvironmentSingleton
    ):
        a = '${TEST1}'
        actual = await env_singleton.substr_env_key(a)
        assert actual == 'TEST1'
