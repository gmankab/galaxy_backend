import os


class env:
    game_url: str = 'https://gmankab.github.io/galaxy_frontend'
    db_url: str = 'sqlite://:memory:'
    tg_token: str = ''
    tests: str = ''
    channel_username: str = '@foo'
    clicks_count: int = 100
    clicks_interval: int = 1


def set_env():
    for key, value_type in env.__annotations__.items():
        value = os.getenv(key)
        if value:
            assert isinstance(value, value_type)
            setattr(env, key, value)


set_env()

