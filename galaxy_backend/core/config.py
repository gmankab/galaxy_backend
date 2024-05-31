import os


class tg:
    token: str


class web:
    url = 'https://gmanka.gitlab.io/galaxy_frontend'


def main():
    token = os.getenv('tg_token')
    assert isinstance(token, str)
    tg.token = token

main()

