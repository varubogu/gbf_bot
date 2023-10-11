class EnvironmentNotFoundException(Exception):
    def __init__(self, *args, **kwargs):
        env_key = kwargs.get('env_key')
        self.message = f'Environment variable {env_key} not found'
