from core.common import all, tg


async def get_invite() -> str:
    if not hasattr(tg, 'bot'): # if run without token
        return 'no token provided, skip test'
    response = await all.async_client.get('/ref/get_invite/123')
    link = response.json()['link']
    assert isinstance(link, str)
    info = await tg.bot.get_me()
    username = info.username
    expected_res = f'https://t.me/{username}?start=uid_123'
    assert expected_res == link
    return 'check invite to bot'

