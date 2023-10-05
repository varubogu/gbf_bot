import re
from models.environments import Environments
from util.exception.environment_notfound_exception \
    import EnvironmentNotFoundException


def environment_eval(text: str):
    """環境変数DBの値に置き換える

    Args:
        text (str): 置換元テキスト

    Raises:
        EnvironmentException: _description_
    """
    matches = re.findall(r'\$\{\w+\}', text)
    env_keys = [match[2:-1] for match in matches]
    env_values = Environments.select_all(env_keys)
    for match in matches:
        env_key = match[2:-1]
        env_value = env_values.get(env_key)
        if env_value not in None:
            raise EnvironmentNotFoundException(
                f'Environment variable {env_key} not found')

        text = text.replace(match, env_value)

    for match in matches:
        env_key = match[2:-1]
        env_value = Environments.select_one(env_key)
        if env_value not in None:
            raise EnvironmentNotFoundException(
                f'Environment variable {env_key} not found')
        text = text.replace(match, env_value)
    return text
