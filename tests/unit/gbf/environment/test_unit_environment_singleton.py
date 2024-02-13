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
    async def test_set_get(
            self,
            env_singleton: EnvironmentSingleton
    ):
        # 追加
        key = "TEST_SET_GET"
        value1 = "KEY1"
        await env_singleton.set(key, value1)
        actual = await env_singleton.get(key)
        assert actual == value1

        # 上書き
        value2 = "KEY2"
        await env_singleton.set(key, value2)
        actual = await env_singleton.get(key)
        assert actual == value2

    @pytest.mark.asyncio
    async def test_get_default(
            self,
            env_singleton: EnvironmentSingleton
    ):
        # デフォルト指定無し
        key = "TEST_GET_DEFAULT"
        actual = await env_singleton.get(key)
        assert actual is None

        # デフォルト指定有り
        value2 = "VALUE2"
        actual = await env_singleton.get(key, value2)
        assert actual == value2

    @pytest.mark.asyncio
    async def test_delete(
            self,
            env_singleton: EnvironmentSingleton
    ):
        # データありの状態にする
        key = "TEST_DELETE"
        value1 = "DELETE1"
        await env_singleton.set(key, value1)
        actual = await env_singleton.get(key)
        assert actual == value1

        await env_singleton.delete(key)
        actual = await env_singleton.get(key)
        assert actual is None

    @pytest.mark.asyncio
    async def test_clear(
            self,
            env_singleton: EnvironmentSingleton
    ):
        # データありの状態にする
        assert len(env_singleton._variables) == 2

        await env_singleton.clear()
        assert len(env_singleton._variables) == 0

    @pytest.mark.asyncio
    async def test_replace_env_eval(
            self,
            env_singleton: EnvironmentSingleton
    ):
        # 変数無し
        actual = await env_singleton.replace_env_eval('abc')
        assert actual == 'abc'

        # 変数１つ
        actual = await env_singleton.replace_env_eval('ab${TEST1}c')
        assert actual == 'ab1c'

        # 変数１種類２回
        actual = await env_singleton.replace_env_eval('ab${TEST1}cd${TEST1}e')
        assert actual == 'ab1cd1e'

        # 変数２種類
        actual = await env_singleton.replace_env_eval('ab${TEST1}cd${TEST2}e')
        assert actual == 'ab1cd2e'

    @pytest.mark.asyncio
    async def test_find_env_keys(
            self,
            env_singleton: EnvironmentSingleton
    ):
        # マッチ無し
        a = 'abcdef'
        actual = await env_singleton.find_env_keys(a)
        assert len(actual) == 0

        # １つマッチ
        a = 'abc${TEST1}def'
        actual = await env_singleton.find_env_keys(a)
        assert len(actual) == 1
        assert actual[0] == "${TEST1}"

        # ２つマッチ
        a = 'abc${TEST1}de${TEST2}f'
        actual = await env_singleton.find_env_keys(a)
        assert len(actual) == 2
        assert actual[0] == "${TEST1}"
        assert actual[1] == "${TEST2}"

        # '$'が無い場合
        a = 'abc${TEST1}de{TEST2}f'
        actual = await env_singleton.find_env_keys(a)
        assert len(actual) == 1
        assert actual[0] == "${TEST1}"

    @pytest.mark.asyncio
    async def test_substr_env_key(
            self,
            env_singleton: EnvironmentSingleton
    ):
        a = '${TEST1}'
        actual = await env_singleton.substr_env_key(a)
        assert actual == 'TEST1'
