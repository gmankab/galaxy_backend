from core.common import all, tg
from models.db import User, Clan, ClanOwner
import api.clans

async def init():
    user1 = await User.create(tg_id=1, coins=100)
    user2 = await User.create(tg_id=2, coins=200)
    user3 = await User.create(tg_id=3, coins=300)
    user4 = await User.create(tg_id=4, coins=400)
    user5 = await User.create(tg_id=5, coins=500)
    user6 = await User.create(tg_id=6, coins=600)
    user7 = await User.create(tg_id=7, coins=700)
    user8 = await User.create(tg_id=8, coins=800)
    user9 = await User.create(tg_id=9, coins=900)
    clanA = await api.clans.create_clan('ClanA', user1.tg_id)
    clanB = await api.clans.create_clan('ClanB', user2.tg_id)
    clanC = await api.clans.create_clan('ClanC', user3.tg_id)
    await api.clans.add_user(clanA.id, user4.tg_id)
    await api.clans.add_user(clanA.id, user5.tg_id)
    await api.clans.add_user(clanB.id, user6.tg_id)
    await api.clans.add_user(clanB.id, user7.tg_id)
    await api.clans.add_user(clanC.id, user8.tg_id)
    await api.clans.add_user(clanC.id, user9.tg_id)


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
    await list_clans()
    clans = await Clan.all()
    for clan in clans:
        await get_invite(clan)
    user4 = await User.filter(tg_id=4).first()
    user6 = await User.filter(tg_id=6).first()
    user8 = await User.filter(tg_id=8).first()
    assert isinstance(user4, User)
    assert isinstance(user6, User)
    assert isinstance(user8, User)
    clanA = await Clan.filter(name='ClanA').first()
    clanB = await Clan.filter(name='ClanB').first()
    clanC = await Clan.filter(name='ClanC').first()
    assert isinstance(clanA, Clan)
    assert isinstance(clanB, Clan)
    assert isinstance(clanC, Clan)
    await remove_user(user4)
    await remove_user(user6)
    await remove_user(user8)
    await create_clan('ClanD', user4)
    await get_owner(clanA)
    await get_owner(clanB)
    await get_owner(clanC)
    await api.clans.add_user(clanA.id, user6.tg_id)
    clanD = await Clan.filter(name='ClanD').first()
    assert isinstance(clanD, Clan)
    await get_members(clanA)
    await get_members(clanB)
    await get_members(clanD)
    await deinit()
    return 'check clans fastapi functions'


async def list_clans():
    response = await all.async_client.get('/clan/list')
    assert response.status_code == 200
    data = response.json()
    expected_result = {'clan2': {'id': 2, 'name': 'ClanA'}, 'clan3': {'id': 3, 'name': 'ClanB'}, 'clan4': {'id': 4, 'name': 'ClanC'}}
    assert data == expected_result


async def get_invite(clan: Clan):
    if not hasattr(tg, 'bot'): # if run without token
        return
    info = await tg.bot.get_me()
    username = info.username
    expected_result = f'https://t.me/{username}?start=joinclan_{clan.id}'
    response = await all.async_client.get(f'/clan/get_invite/{clan.id}')
    assert response.status_code == 200
    msg = response.json()
    assert isinstance(msg, dict)
    link = msg['link']
    assert isinstance(link, str)
    assert link == expected_result


async def remove_user(user: User):
    await user.fetch_related('clan')
    clan = user.clan
    assert isinstance(clan, Clan)
    members_expected = await api.clans.get_members(clan.id)
    members_expected.remove(user)
    id = user.tg_id
    payload = {'user_id': id}
    response = await all.async_client.post('/clan/member/remove', json=payload)
    assert response.status_code == 200
    data = response.json()
    expected_result = {'message': 'User removed from clan'}
    assert data == expected_result
    members_new = await api.clans.get_members(clan.id)
    assert members_expected == members_new


async def create_clan(name: str, owner: User):
    payload = {'clan_name': name, 'clan_owner_id': owner.tg_id}
    response = await all.async_client.post('/clan/create', json=payload)
    assert response.status_code == 200
    msg = response.json()
    clan_from_db = await Clan.filter(name=name).first()
    assert isinstance(clan_from_db, Clan)
    await api.clans.get_owner(clan_from_db.id)
    response_expected = {'clan_id': clan_from_db.id, 'clan_name': name}
    assert msg == response_expected


async def get_owner(clan: Clan):
    response = await all.async_client.get(f'/clan/get_owner/{clan.id}')
    assert response.status_code == 200
    owner_from_db = await api.clans.get_owner(clan.id)
    msg = response.json()
    assert isinstance(msg, dict)
    owner_id = msg['clan_owner_id']
    assert isinstance(owner_id, int)
    assert owner_id == owner_from_db


async def get_members(clan: Clan):
    response = await all.async_client.get(f'/clan/member/list/{clan.id}')
    assert response.status_code == 200
    msg = response.json()
    assert isinstance(msg, dict)
    members_from_db = await api.clans.get_members(clan.id)
    members_from_db_id = []
    for member in members_from_db:
        members_from_db_id.append(member.tg_id)
    members = msg['members']
    assert isinstance(members, list)
    members.sort()
    members_from_db_id.sort()
    assert members == members_from_db_id

