import asyncio
import re
from gbf import models

from gbf.utils.exception.environment_notfound_exception \
    import EnvironmentNotFoundException


class EnvironmentSingleton:

    _instance: 'EnvironmentSingleton' = None
    _lock = asyncio.Lock()

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(EnvironmentSingleton, cls).__new__(cls)
            cls._instance._variables: dict = {}
        return cls._instance

    async def set(self, key, value):
        async with self._lock:
            self._variables[key] = value

    async def get(self, key, default=None):
        async with self._lock:
            return self._variables.get(key, default)

    async def delete(self, key):
        async with self._lock:
            if key in self._variables:
                del self._variables[key]

    async def clear(self):
        async with self._lock:
            self._variables.clear()

    async def load_db(self, session):
        async with self._lock:
            self._variables.clear()

            db_envs = await models.Environments.select_all(session)
            for db_env in db_envs:
                self._variables[db_env.key] = db_env.value

    async def replace_env_eval(self, text: str):
        """環境変数DBの値に置き換える

        Args:
            text (str): 置換元テキスト

        Raises:
            EnvironmentException: _description_
        """
        err_keys = []
        async with self._lock:
            matches = await self.find_env_keys(text)
            for match in matches:
                env_key = await self.substr_env_key(match)
                env_value = self._variables.get(env_key, None)
                if env_value is None:
                    err_keys.append(env_key)
                else:
                    text = text.replace(match, env_value)

        if err_keys:
            err_keys_str = ','.join([key for key in err_keys])
            raise EnvironmentNotFoundException(env_key=err_keys_str)

        return text

    async def find_env_keys(self, text: str):
        """文字列の中から埋め込み変数を探し、リストを返す

        Args:
            text (str): 対象文字列 aaa${variable1}bbb${variable2}

        Returns:
            _type_: ["${variable1}", "${variable2}"]
        """
        return re.findall(r'\$\{\w+\}', text)

    async def substr_env_key(self, variable_str: str) -> str:
        """変数文字列からkeyを取得する

        Args:
            variable_str (str): 対象文字列 例: ${abc}

        Returns:
            str: 変数書式を取り除いたkey 例: abc
        """
        return variable_str[2:-1]
