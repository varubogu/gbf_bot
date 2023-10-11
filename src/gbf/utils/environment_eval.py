import re
from gbf.models.environments import Environments
from gbf.utils.exception.environment_notfound_exception \
    import EnvironmentNotFoundException


async def environment_eval(text: str):
    """環境変数DBの値に置き換える

    Args:
        text (str): 置換元テキスト

    Raises:
        EnvironmentException: _description_
    """
    matches = find_env_keys(text)
    env_keys = await [substr_env_key(match) async for match in matches]
    env_list = await Environments.select_all(env_keys)
    for match in matches:
        env_key = substr_env_key(match)
        env_value = env_list.get(env_key)
        if env_value not in None:
            raise EnvironmentNotFoundException(env_key=env_key)

        text = text.replace(match, env_value)
    return text


async def find_env_keys(text: str):
    return re.findall(r'\$\{\w+\}', text)


async def substr_env_key(matched_str: str):
    return matched_str[2:-1]
