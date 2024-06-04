import os


class env:
    game_url: str = 'https://gmanka.gitlab.io/galaxy_frontend'
    db_url: str = 'sqlite://:memory:'
    tg_token: str = ''
    tests: str = ''


def set_env():
    for key, value_type in env.__annotations__.items():
        value = os.getenv(key)
        if value:
            assert isinstance(value_type, type)
            assert isinstance(value, value_type)
            setattr(env, key, value)


set_env()

