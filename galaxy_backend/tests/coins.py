from core.common import all
import models.db


async def get_coins() -> str:
    params = {'tg_id': 0}
    response = await all.async_client.get(
        '/coin/get',
        params=params,
    )
    data = response.json()
    assert response.status_code == 200
    assert data['coins'] == 0
    return 'coins get'


async def add_coins():
    json = {
        'tg_id': 0,
        'amount': 50,
    }
    response = await all.async_client.post(
        '/coin/add',
        json=json,
    )
    data = response.json()
    assert response.status_code == 200
    assert data["success"] is True
    updated_user = await models.db.User.get(tg_id=0)
    assert updated_user.coins == 50
    return 'coins add'


async def start_autoclick():
    params = {
        'tg_id': 0,
    }
    response = await all.async_client.get(
        '/coin/autoclick',
        params=params
    )
    data = response.json()
    assert response.status_code == 200
    assert data["success"] is True
    return 'autoclick'

