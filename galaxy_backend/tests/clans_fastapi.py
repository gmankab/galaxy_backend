from core.common import all
from models.db import User, Clan, ClanOwner
import api.clans

async def init():
    user1 = await User.create(tg_id=1)
    user2 = await User.create(tg_id=2)
    user3 = await User.create(tg_id=3)
    user4 = await User.create(tg_id=4)
    user5 = await User.create(tg_id=5)
    user6 = await User.create(tg_id=6)
    user7 = await User.create(tg_id=7)
    user8 = await User.create(tg_id=8)
    user9 = await User.create(tg_id=9)
    clanA = await api.clans.create_clan('ClanA', user1.tg_id)
    clanB = await api.clans.create_clan('ClanB', user2.tg_id)
    clanC = await api.clans.create_clan('ClanC', user3.tg_id)
    await api.clans.add_user(user4.tg_id, clanA.id)
    await api.clans.add_user(user5.tg_id, clanA.id)
    await api.clans.add_user(user6.tg_id, clanB.id)
    await api.clans.add_user(user7.tg_id, clanB.id)
    await api.clans.add_user(user8.tg_id, clanC.id)
    await api.clans.add_user(user9.tg_id, clanC.id)


async def deinit():
    clans = await Clan.all()
    clan_owners = await ClanOwner.all()
    users = await User.all()
    for clan_owner in clan_owners:
        await clan_owner.delete()
    for user in users:
        await user.delete()
    for clan in clans:
        await clan.delete()


async def run_tests() -> str:
    await init()
    list_clans_res = await list_clans()
    if list_clans_res != 'success':
        await deinit()
        raise Exception(list_clans_res)
    await deinit()
    return list_clans_res
    return 'check clans fastapi functions'


async def list_clans() -> str:
    response = await all.async_client.get('/clan/list')
    try:
        assert response.status_code == 200
    except AssertionError:
        return 'list_clans(): response status code is not 200'
    data = response.json()
    return data

